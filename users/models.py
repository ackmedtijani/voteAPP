from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin

from .managers import CustomUserManager


class CustomUsers(AbstractBaseUser  , PermissionsMixin):
    name = models.CharField(max_length=500 , blank=False , null = False)
    email = models.EmailField(max_length=255 , blank=False ,
                              null=False , unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ "name" , "password"]

# Create your models here.
