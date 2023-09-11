from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profile_main_user_data/', views.profile_main_user_data, name='profile_main_user_data'),
    path('profile_main_user_data_form/', views.profile_main_user_data_form, name='profile_main_user_data_form'),
]
