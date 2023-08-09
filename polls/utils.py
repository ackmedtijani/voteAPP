from datetime import datetime

from django.core.mail import EmailMessage

from .models import Answers

def convert_to_days(date):
    seconds = datetime.timestamp(date)
    
def convert_to_answer(lists):
    answers = []
    for x ,y in lists.items():
        for dat in y:
            answers.append(Answers.objects.get(answers=dat , questions__id = int(x)))
    return answers
    

def send_mail(subject, body, to_email ,  host=None, attach_file = None):
    from_email = host if host else "settings.EMAIL_FROM"
    
    msg = EmailMessage(subject, body , from_email , [to_email])
    
    if attach_file:
        msg.content_subtype = "html"  
        msg.attach_file('pdfs/Instructions.pdf')
        
    msg.send()

