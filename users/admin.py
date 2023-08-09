from django.contrib import admin

from .models import CustomUsers

# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    model = CustomUsers
    
admin.site.register(CustomUsers , UsersAdmin)