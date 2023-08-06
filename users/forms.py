
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm ,\
    PasswordChangeForm , PasswordResetForm)
from .models import CustomUsers



class CustomCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUsers
        fields = ('name', 'email' )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsers
        fields = ('name' ,'email')
        
class CustomPasswordChangeForm(PasswordChangeForm):
    pass


