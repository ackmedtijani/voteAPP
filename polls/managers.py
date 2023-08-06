from django.db import models

class AnswersManager(models.Manager):
    def find_related_answers(self , questions):
        lookups = models.Q(questions__id = questions.id)
        return self.get_queryset().filter(lookups)