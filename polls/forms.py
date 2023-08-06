from django.forms import ModelForm , inlineformset_factory
from .models import (Poll , Answers , Questions , 
                     PollsMetaData)




class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = '__all__'


class QuestionForm(ModelForm):
    class Meta:
        model = Questions
        fields = '__all__'


class AnswerForm(ModelForm):
    class Meta:
        model = Answers
        exclude = ['number_times_chosen']

class PollsMetaData(ModelForm):
    class Meta:
        model = PollsMetaData
        fields = '__all__'
        


QuestionsFormset = inlineformset_factory(Questions, Answers , form = AnswerForm , 
                                         extra=5)