from django import forms
from django.contrib.auth.models import User
from rango.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password')
        
class UserProfileForm(forms.ModelForm):
    show_email = forms.BooleanField(required=False)
        
    class Meta:
        model = UserProfile
        fields = ('show_email', 'website',)

