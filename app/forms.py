from django import forms
from .models import CarpetType
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CarpetTypeForm(forms.ModelForm):
    class Meta:
        model = CarpetType
        fields = ['name', 'description', 'price_per_m2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gilam nomi'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tavsif'}),
            'price_per_m2': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Narx'}),
        }

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        max_length=150,
        help_text="Faqat harflar, raqamlar va @/./+/-/_ belgilari ishlatilishi mumkin."
    )
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput,
        help_text="Parol kamida 8 ta belgidan iborat bo‘lishi, shaxsiy ma’lumotlarga o‘xshamasligi va raqamlar bilan cheklanmasligi kerak."
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlash",
        widget=forms.PasswordInput,
        help_text="Yuqoridagi parolni takror kiriting."
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")