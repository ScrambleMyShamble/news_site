from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .forms import UserRegisterForm, UserLoginForm, ContactForm


# регистрация через django класс UserCreationForm
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка при регистрации!')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


# отправка email
def mail_send(request):
    if request.method == 'POST':
        # ContactForm - форма email, с полями subject - тема письма и content - текст письма.
        form = ContactForm(data=request.POST)
        if form.is_valid():
            # настройки по отправке писем прописываются в settings, EMAIL_HOST_USER - эл.почта, с которой
            # будет отправляться письмо
            # в метод send_mail нужно указать тему письма, текст, почта-отправитель, почта-получатель
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], from_email='почта-отправитель',
                             recipient_list=['список почта-получатель'], fail_silently=False)
            # если fail_silently=True, вывод нашей ошибки
            if mail:
                messages.success(request, 'Письмо отправлено!')
            else:
                messages.error(request, 'Ошибка отправки')
        # если форма не валидна
        else:
            messages.error(request, 'Ошибка в форме')
    # если метод GET
    else:
        form = ContactForm()
    return render(request, 'user/send_mail.html', {'form': form})
