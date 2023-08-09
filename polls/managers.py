from django.db import models

class AnswersManager(models.Manager):
    def find_related_answers(self , questions):
        lookups = models.Q(questions__id = questions.id)
        return self.get_queryset().filter(lookups)
    
class RespondentsManager(models.Manager):
    def group_by_respondents(self, poll = None, id = None):
        if poll is not None or id is not None:
            print("Poll ," , poll)
            queryset = self.get_queryset().filter(poll = poll)
            dataframe = {}
            for query in queryset:
                dataframe[query.respondent] = query.question_answer_pair() 
            return dataframe
        else:
            raise KeyError("Poll and Poll primary key not supplied")