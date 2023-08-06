from .models import Questions, Answers

class OwnerAllowedMixin:
    
    def check_owner(self , request , model):
        if request.user_authenticated and model.objects.get(ownwer = request.user):
            return True
        return False
        
class UserDetailMixin:
    def get_user_object(self , request):
        return request.user

class GetPollsDataMixin:
        
    def get_related(self , poll):
        ques = Questions.objects.filter(poll = poll)
        result = [{i : Answers.objects.filter(questions = i)} for i in ques]
        
        return result