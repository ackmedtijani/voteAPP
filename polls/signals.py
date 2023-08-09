from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Poll , PollsMetaData

@receiver(post_save , sender = Poll)
def create_metadata(sender , instance, created , **kwargs):
    if created:
        PollsMetaData.objects.create(polls = instance)
