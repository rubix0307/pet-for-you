from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('auth/', views.user_auth, name='user_auth'),
    path('logout/', views.user_logout, name='logout'),
]


urlpatterns_htmx = [
    path('profile_main_user_data/', views.profile_main_user_data, name='profile_main_user_data'),
    path('profile_main_user_data_form/', views.profile_main_user_data_form, name='profile_main_user_data_form'),

    path('auth/sign_in/', views.user_sign_in, name='user_sign_in'),
    path('auth/register/', views.user_register, name='user_register'),
]
urlpatterns += urlpatterns_htmx