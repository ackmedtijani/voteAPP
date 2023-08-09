from django.urls import path , re_path
from .views import (listvotes , vote_detail, UpdatePollView ,\
    CreateQuestionsViews , EditQuestionsView , CreatePollView , 
    generate_report_view)

urlpatterns = [
    
    path('' , listvotes , name ="home"),
    path('<int:pk>/' , vote_detail , name="vote-detail"),
    path('create/' , CreatePollView.as_view() , name = "create_poll"),
    path('<int:pk>/update_polls' , UpdatePollView.as_view() , name = "update_poll"),
    path('create_questions/' , CreateQuestionsViews.as_view() , name = "create_questions"),
    path('update_questions/<int:pk>' , EditQuestionsView.as_view() , name = 'update_questions'),
    path('<int:pk>/generate_report',generate_report_view , name = "generate_report" )
]