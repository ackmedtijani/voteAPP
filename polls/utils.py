from datetime import datetime
from .models import Answers

def convert_to_days(date):
    seconds = datetime.timestamp(date)
    

def get_report_per_poll(poll):
    questions = [get_make_reports(questions) for questions in poll.questions_set.all()]
    return {'title' : [poll.title] , 
            'days_opened' : [poll.deadline - poll.created],
            'questions' : [questions.title for questions in poll.questions_set.all()],
            'questions_statistics' : questions
        }        


def get_make_reports(questions):
    answers = questions.answers_set.all()
    return {ans.name :ans.number_chosen for ans in answers}
    #get percentage of each questions. 
    
def convert_to_answer(lists):
    answers = []
    for x ,y in lists.items():
        for dat in y:
            answers.append(Answers.objects.get(answers=dat , questions__id = int(x)))
    return answers
    
    

