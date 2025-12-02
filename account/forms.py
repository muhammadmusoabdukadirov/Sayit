from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import re

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    password1 = forms.CharField(label="Parol", widget=forms.PasswordInput(attrs={'placeholder':'Parol'}), required=True)
    password2 = forms.CharField(label="Parolni tasdiqlash", widget=forms.PasswordInput(attrs={'placeholder':'Parolni tasdiqlash'}), 
                required=True
    )

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar mos kelmadi!")
        if not re.search(r'[A-Za-z]', password1):
            raise forms.ValidationError("Parolda kamida bitta harf bo`lishi kerak!")
        if not re.search(r'\d', password1):
            raise forms.ValidationError("Parolda kamida bitta raqam bo`lishi kerak!")
        if len(password1) < 8:
            raise forms.ValidationError("Parol kamida 8 belgidan iborat bo`lishi kerak!")
        return password2

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Parol'}))
