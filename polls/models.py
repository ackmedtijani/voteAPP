from django.db import models
from django.contrib.auth import get_user_model


from .managers import AnswersManager , RespondentsManager

User = get_user_model()

class Poll(models.Model):
    owner = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=500 , blank=False , null=False)
    created = models.DateTimeField(auto_created=True)
    deadline = models.DateTimeField()
    deadline_reached = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"
    
    
class PollsMetaData(models.Model):
    polls = models.OneToOneField(Poll , related_name="polls_metadata",
                                 on_delete=models.CASCADE , 
                                 blank=False , null=False)
    number_of_visits = models.IntegerField(
                                          default=0)
    number_of_submits = models.IntegerField( 
                                            default=0)
    
    class Meta:
        ordering = ['number_of_submits' , 'number_of_visits']
        indexes = [
            models.Index(fields = ['number_of_submits',
                                   'number_of_visits'])
        ]

class Questions(models.Model):
    poll = models.ForeignKey(Poll , related_name="poll_questions",
                             blank=False , null=False , on_delete=models.CASCADE)
    questions = models.CharField(max_length = 500 , blank=False ,
                                 null=False)
    multiple_answer = models.BooleanField(default=False)
    order = models.IntegerField(blank=True , null=True)
    
    def __str__(self):
        return f"{self.questions}"
    
    def save(self, **kwargs) -> None:
        if self.order is None:
            try:
                questions = Questions.objects.filter(poll == self.poll).last()
                self.order = models.F(questions.order) + 1
            except Questions.DoesNotExist as e:
                self.order = 1
    
        return super().save(**kwargs)
            
            
    

class Answers(models.Model):
    questions = models.ForeignKey(Questions, related_name="question_answers",
                                  null=False , blank=False , on_delete=models.CASCADE)
    answers = models.CharField(max_length=255 , null=False , blank=False)
    number_times_chosen = models.IntegerField(
                                              default=0)
    order = models.IntegerField(blank=True , null=True)
    all_or_none = models.BooleanField(default=False)
    
    objects = AnswersManager()
    
    class Meta:
        indexes = [
            models.Index(fields = ['answers'])
        ]
    
    def __str__(self):
        return f"{self.answers}"
    
    
    def clean(self) -> None:
        '''
            Setting all_or_none = models.BooleanField to true or false based on 
            the value in the answers charfield. 
        '''
        return super().clean()
    
    def save(self, **kwargs) -> None:
        if self.order is None:
            try:
                answers = Answers.objects.filter(questions = self.questions).last()
                answers = models.F(answers.order) + 1
            except Answers.DoesNotExist as e:
                self.order = 1
        
        return super().save(**kwargs)
        
    @property
    def increase_ntb(self):
        self.number_times_chosen += 1
        return self
    
class Respondents(models.Model):
    respondent = models.ForeignKey(User , on_delete= models.CASCADE ,
                                   related_name="poll_respondent")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE , related_name="poll_answered")
    answers = models.ManyToManyField(Answers , related_name="answer_chosen")
    
    objects = RespondentsManager()
    
    class Meta:
        ordering = ['respondent']
        indexes = [
            models.Index(fields = ['poll'])
        ]
    
    def __str__(self) -> str:
        return f"{self.respondent} Poll {self.poll}"
    
    def question_answer_pair(self):
        ques_ans = {}
        print(self.answers.all())
        for i in self.answers.all():
            order = "Q" + str(i.questions.order)
            
            if order not in ques_ans:
                ques_ans[order] = i.answers + " "
            else:
                ques_ans[order] += i.answers + " "
        
        return ques_ans
    
