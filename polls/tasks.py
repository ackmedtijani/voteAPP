from celery import shared_task
import asyncio
import pandas as pd
from datetime import  timedelta

from django.core.cache import cache
from django.utils import timezone

from .models import Poll , Respondents
from .utils import send_mail


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
                asyncio.run(async_sleep(time_taken))
    else:
        pass
    

@shared_task
def generate_report(poll):
    dataframe = Respondents.objects.group_by_respondents(poll=poll)
    pf = pd.DataFrame(dataframe).T
    print("DataFrame" , pf)
    file = pf.to_csv(f"static/reports/{poll.name}.csv")
    send_mail("Polls report" , "This is a poll for the part of the comp",
              poll.owner.email , attach_file=file)

    
    
    
    
   

    
    