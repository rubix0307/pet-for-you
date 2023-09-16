import time
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserSignInForm


@login_required(login_url='user_auth')
def profile(request: WSGIRequest):
    return render(request, 'user/profile.html')

@login_required(login_url='user_auth')
def profile_main_user_data(request: WSGIRequest):
    return render(request, 'user/inc/_profile_main_user_data.html')

@login_required(login_url='user_auth')
def profile_main_user_data_form(request: WSGIRequest):
    return render(request, 'user/inc/_profile_main_user_data_form.html')


def user_auth(request: WSGIRequest):
    form = UserSignInForm()

    return render(request, 'user/auth.html', context=dict(form=form))

def user_sign_in(request):
    if request.method == 'POST':
        form = UserSignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            authenticated_user = authenticate(request, email=email, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('profile')

    else:
        form = UserSignInForm()

    return render(request, 'user/inc/_sign_in_form.html', context=dict(form=form))

def user_register(request: WSGIRequest):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

            authenticated_user = authenticate(email=user.email, password=form.cleaned_data['password'])
            if authenticated_user:
                login(request, authenticated_user)

            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/inc/_register_form.html', context=dict(form=form))

@login_required(login_url='user_auth')
def user_logout(request: WSGIRequest):
    logout(request)
    return redirect('main')

