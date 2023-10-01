from enum import Enum
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserLoginForm


@login_required(login_url='user_auth')
def profile(request: WSGIRequest):
    return render(request, 'user/profile.html')

def get_profile_main_html_data(request: WSGIRequest):
    return render(request, 'user/inc/_profile_main_data.html')

def get_profile_main_html_form(request: WSGIRequest):
    return render(request, 'user/inc/_profile_main_data_form.html')


class FormNames(Enum):
    LOGIN = "login_form"
    REGISTER = 'registration_form'

def get_login_html_form(request: WSGIRequest):
    return render(request, 'user/inc/_login_form.html', context=dict(form=UserLoginForm(), form_name=FormNames.LOGIN.value))

def get_register_html_form(request: WSGIRequest):
    return render(request, 'user/inc/_register_form.html', context=dict(form=RegistrationForm(), form_name=FormNames.REGISTER.value))

def user_auth(request: WSGIRequest):
    context = dict(FormNames=FormNames)

    if request.method == 'POST':
        if FormNames.LOGIN.value in request.POST:
            context['form_name'] = FormNames.LOGIN.value

            form = UserLoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('profile')
                else:
                    form.add_error(None, 'Неверный email или пароль')

        elif FormNames.REGISTER.value in request.POST:
            context['form_name'] = FormNames.REGISTER.value

            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('profile')
    else:
        context['form_name'] = FormNames.LOGIN.value
        context['form'] = UserLoginForm()

    return render(request, 'user/auth.html', context=context)

@login_required(login_url='user_auth')
def user_logout(request: WSGIRequest):
    logout(request)
    return redirect('main')

