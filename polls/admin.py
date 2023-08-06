from django.contrib import admin
from .models import Answers , Questions, Poll , PollsMetaData , Respondents
from .forms import AnswerForm , QuestionForm , PollForm , PollsMetaData 



class AnswerInline(admin.TabularInline):
    model = Answers
    form = AnswerForm
    
class QuestionsAdmin(admin.ModelAdmin):
    form = QuestionForm
    model = Questions
    list_filter = ('poll',)
    inlines = [AnswerInline]
    
class PollAdmin(admin.ModelAdmin):
    form = PollForm
    model = Poll
    list_display = ('id',)
    list_filter = ("owner",)
    
class AnswerAdmin(admin.ModelAdmin):
    form = AnswerForm
    model = Answers

class RespondentsAdmin(admin.ModelAdmin):
    model = Respondents
    
admin.site.register(Questions , QuestionsAdmin)
admin.site.register(Poll , PollAdmin)
admin.site.register(Answers , AnswerAdmin)
admin.site.register(Respondents , RespondentsAdmin)



# Register your models here.
