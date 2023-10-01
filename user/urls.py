from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
]


urlpatterns_htmx = [
    path('htmx/profile_main_user_data/', views.get_profile_main_html_data, name='profile_main_user_data'),
    path('htmx/profile_main_user_data_form/', views.get_profile_main_html_form, name='profile_main_user_data_form'),

    path('htmx/user_login_html_form/', views.get_login_html_form, name='user_login_html_form'),
    path('htmx/user_register_html_form/', views.get_register_html_form, name='user_register_html_form'),
]
urlpatterns += urlpatterns_htmx