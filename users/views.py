from django.shortcuts import render , redirect
from django.views import generic
from django.contrib.auth import authenticate , login, get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse

from .models import CustomUsers
from .forms import CustomCreationForm

# Create your views here.

User= get_user_model()

class SignUpView(generic.CreateView):
    model = CustomUsers
    form_class = CustomCreationForm
    template_name = "auth/signup.html"

class SigninView(LoginView):
    template_name = "auth/login.html"
   
    def get_success_url(self) -> str:
        return reverse('user_page' , kwargs={'pk' : self.user.id})
    
    def form_valid(self, form):
        self.user = form.get_user()
        return super().form_valid(form)
    


class UserView(generic.DetailView):
    model = User
    template_name = 'users/user_page.html'
    """
        Displays the list of polls for a particular user
    """
    
    def get_polls(self, objects):
        return objects.poll_set.all()
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['polls'] = self.get_polls(self.get_object())
        print(context)
        return context

'''
    A poll should have 
'''


