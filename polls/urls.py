from django.urls import path 
from .views import (listvotes , vote_detail, UpdatePollView ,\
    CreateQuestionsViews , EditQuestionsView , CreatePollView)

urlpatterns = [
    
    path('' , listvotes , name ="home"),
    path('<int:pk>/' , vote_detail , name="vote-detail"),
    path('create/' , CreatePollView.as_view() , name = "create_poll"),
    path('update_poll/<int:pk>/' , UpdatePollView.as_view() , name = "update_poll"),
    path('create_questions/' , CreateQuestionsViews.as_view() , name = "create_questions"),
    path('update_questions/<int:pk>' , EditQuestionsView.as_view() , name = 'update_questions')
]