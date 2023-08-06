from django.urls import path 
from .views import SigninView , SignUpView , UserView


urlpatterns = [
    path("login/" , SigninView.as_view() , name = "login"),
    path("register/",  SignUpView.as_view() , name = "register" ),
    path('<int:pk>/' , UserView.as_view() , name = 'user_page')
]