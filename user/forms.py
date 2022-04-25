from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField, CaptchaTextInput


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = User
        # порядок полей в форме
        fields = ('username', 'email', 'password1', 'password2')


# форма по отправке email
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=150, label='Тема письма',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(max_length=150, label='Текст',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()
