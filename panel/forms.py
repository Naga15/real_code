from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}),label='Username',initial='riemann')
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}),initial='password')
    
      
    def clean(self, *args, **kwargs):
         username = self.cleaned_data.get("username")
         password = self.cleaned_data.get("password")
         return True
         '''
         if username and password:
            info = User.objects.filter(username=username, groups__name='Client').first()
            if not info:
               raise ValidationError("This username does not exists")
            user = authenticate(username=info.username, password=password)
            if not user:
               raise ValidationError("This password is invalid")
            return True
         '''