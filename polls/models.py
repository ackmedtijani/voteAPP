from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


from .managers import AnswersManager

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
    
    def __str__(self):
        return f"{self.questions}"
    

class Answers(models.Model):
    questions = models.ForeignKey(Questions, related_name="question_answers",
                                  null=False , blank=False , on_delete=models.CASCADE)
    answers = models.CharField(max_length=255 , null=False , blank=False)
    number_times_chosen = models.IntegerField(
                                              default=0)
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
    
    @property
    def increase_ntb(self):
        self.number_times_chosen += 1
        return self
    
class Respondents(models.Model):
    respondent = models.ForeignKey(User , on_delete= models.CASCADE ,
                                   related_name="poll_respondent")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE , related_name="poll_answered")
    answers = models.ForeignKey(Answers, on_delete= models.DO_NOTHING , related_name="answer_chosen")
    
    class Meta:
        ordering = ['respondent']
        indexes = [
            models.Index(fields = ['poll'])
        ]
    
    def __str__(self) -> str:
        return f"{self.respondent} Poll {self.poll}"
    
@receiver(post_save , sender = Poll)
def create_metadata(sender , instance, created , **kwargs):
    if created:
        PollsMetaData.objects.create(polls = instance)