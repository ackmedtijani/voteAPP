from celery import shared_task
import time
import asyncio
from datetime import  timedelta

from django.core.cache import cache
from django.utils import timezone
from django.core.mail import send_mail

from .models import Poll
from .utils import get_report_per_poll


async def async_sleep(number):
    await asyncio.sleep(number)

def check_time(poll):
    if poll.deadline <= timezone.now():
        return True
    return False

    
@shared_task
def check_deadline():
    polls = Poll.objects.filter(deadline__lt = 
                                timezone.now() + timedelta(days=1)).order_by('deadline')


    if polls:
        i = 0
        while i < len(polls):
            if check_time(polls[i]):
                polls[i].deadline_reached = True
                polls[i].save()
                i += 1
                
            else:
                time_taken = polls[i].deadline.timestamp()
                time.sleep
                asyncio.run(async_sleep(time_taken))
    else:
        pass
    

@shared_task
def generate_report(poll):
    poll_name = poll.name.replace(" ", "")
    dicts = get_report_per_poll(poll)
    '''
    pf = pd.DataFrame(dicts)
    pf.set_index(["title" , "days_opened" , "questions"] , inplace = True)
    print(pf)
    '''

    
    