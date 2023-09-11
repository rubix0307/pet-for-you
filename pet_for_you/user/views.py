import time

from django.shortcuts import render


def profile(request):
    return render(request, 'user/profile.html')

def profile_main_user_data(request):
    return render(request, 'user/inc/_profile_main_user_data.html')

def profile_main_user_data_form(request):
    return render(request, 'user/inc/_profile_main_user_data_form.html')