from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserSignInForm


@login_required(login_url='user_auth')
def profile(request: WSGIRequest):
    return render(request, 'user/profile.html')

def get_profile_main_html_data(request: WSGIRequest):
    return render(request, 'user/inc/_profile_main_data.html')

def get_profile_main_html_form(request: WSGIRequest):
    return render(request, 'user/inc/_profile_main_data_form.html')

def get_sign_in_html_form(request: WSGIRequest):
    return render(request, 'user/inc/_sign_in_form.html', context=dict(form=UserSignInForm()))

def get_register_html_form(request: WSGIRequest):
    return render(request, 'user/inc/_register_form.html', context=dict(form=UserRegistrationForm()))

def user_auth(request: WSGIRequest):
    form = UserSignInForm()
    return render(request, 'user/auth.html', context=dict(form=form))

def user_sign_in(request: WSGIRequest):
    form = UserSignInForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']

        authenticated_user = authenticate(request, email=email, password=password)
        if authenticated_user:
            login(request, authenticated_user)
            return redirect('profile')
    return user_auth(request)

def user_register(request: WSGIRequest):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.set_password(form.cleaned_data['password'])
        user.save()

        authenticated_user = authenticate(email=user.email, password=form.cleaned_data['password'])
        if authenticated_user:
            login(request, authenticated_user)

        return redirect('profile')

@login_required(login_url='user_auth')
def user_logout(request: WSGIRequest):
    logout(request)
    return redirect('main')

