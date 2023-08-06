import json

from django.shortcuts import render , redirect 
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponse
from django.db.models import F
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .mixins import GetPollsDataMixin
from .forms import (PollForm , AnswerForm, QuestionsFormset,
                    QuestionForm)
from .models import (PollsMetaData , Poll 
                     , Questions , Answers , Respondents)
from .tasks import generate_report
from .utils import convert_to_answer

def listvotes(request):
    
    if request.method == 'GET':
        try:
            newly_created = Poll.objects.all()[:5]
            polls = PollsMetaData.objects.all()[:5]
        except:
            return render(request , "home.html",
                          {"new_polls" : [],
                           "popular_polls" : []})
        return render(request , 'home.html' , {
            'new_polls' : newly_created,
            'popular_polls' : polls,
        })
   
        
@login_required(login_url="login")
def vote_detail(request , *args , **kwargs):
    response = HttpResponse("Good Message")
    id = kwargs.get('pk' , None)
    visits = request.COOKIES.get('visits' , None)
    if visits is None:
        request.session['visit'] = 0
        visits = 0
    if id is None:
            raise Exception("No ID sent")
    try:
            poll = Poll.objects.get(id = id)
            poll_meta_data = PollsMetaData.objects.get(polls = poll)
            objects = [poll , poll_meta_data]
    except:
        raise Exception("No polls or meta_DATA FOUND")
    
    
    if request.method == 'GET':
        print(poll)
        objects[1].number_of_visits += 1
        
        try:
            all_ques = {}
            ques = Questions.objects.filter(poll = objects[0])
            result = [{i : Answers.objects.filter(questions = i)} for i in ques]
        except:
            raise Exception("Questions and Answers not found")
        return render(request , 'vote-detail.html' , 
                    {'ques' : result })
        
    if request.method == "POST":
        data = json.load(request)
        print("Data" , data)
        if int(visits) > 1:
            raise Exception("You have voted already")
        else:
            try:
                if Respondents.objects.filter(respondent = request.user).exists():
                    raise Exception("You have voted pass")
            except Respondents.DoesNotExist as e:
                pass
        
        with transaction.atomic():
            answers = convert_to_answer(data)
            
            res = map(lambda x: Respondents(respondent = request.user , poll=poll , answers = x) , answers)
            Respondents.objects.bulk_create(list(res))

    
        objects[1].number_of_submits +=1 
        response.set_cookie('visits' , str(int(visits) + 1))
        
        return response

'''
        return HttpResponse("Object Received")        

def submit_questions(request , *args , **kwargs):
    pass

def poll_done(request):
    return render(request , "Poll is done")
    
# Create your views here.
'''

class DetailPollView(generic.DetailView):
    pass

class CreatePollView(LoginRequiredMixin
                     ,generic.CreateView):
    form_class = PollForm
    model = Poll
    template_name = "create_poll.html"
    login_url = 'login'

class UpdatePollView(generic.UpdateView , UserPassesTestMixin , GetPollsDataMixin):
    form_class = PollForm
    model = Poll
    template_name = 'update_poll.html'
    
    def test_func(self):
        if self.request.user.is_authenticated and \
        self.model.objects.get(ownwer = self.request.user):
            return True
        return False
    
    def get(self, request, *args: str, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data()
        context['result'] = self.get_related(self.object)
        return self.render_to_response(context)
    

class CreateQuestionsViews(generic.CreateView):
    template_name = 'create_questions.html'
    model = Questions
    form_class = QuestionForm

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = QuestionsFormset()
        return context


    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        questions_formset = QuestionsFormset(self.request.POST)
        if form.is_valid() and questions_formset.is_valid():
            return self.form_valid(form, questions_formset)
        else:
            return self.form_invalid(form, questions_formset)
    
    def form_valid(self, form, formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving ProductMeta Instances
        product_metas = formset.save(commit=False)
        for meta in product_metas:
            meta.product = self.object
            meta.save()
        return redirect(reverse("user_page" , {'pk' : self.request.user.id}))
    
    def form_invalid(self, form, product_meta_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  product_meta_formset=product_meta_formset
                                  )
        )
    

class EditQuestionsView(generic.UpdateView):
    template_name = 'update_questions.html'
    model = Questions
    form_class = QuestionForm
    
    
    def get(self, request, *args: str, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data()
        context['formset'] = context['formset'] = QuestionsFormset(instance = self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        print(self.request.POST)
        
        self.object = self.get_object()
        
        questions_formset = QuestionsFormset(self.request.POST , instance= self.object)
        if form.is_valid() and questions_formset.is_valid():
            return self.form_valid(form, questions_formset)
        else:
            return self.form_invalid(form, questions_formset)
    
    def form_valid(self, form, formset):
        print(form)
        # saving ProductMeta Instances
        product_metas = formset.save(commit=False)
        for meta in product_metas:
            meta.questions = self.object
            meta.save()
        return redirect(reverse("home"))
    
    def form_invalid(self, form, product_meta_formset):
        print("Invalid")
        return self.render_to_response(
            self.get_context_data(form=form,
                                  formset=product_meta_formset
                                  )
        )
