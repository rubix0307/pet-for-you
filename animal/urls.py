from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.animal_index, name='animal_index'),
    path('<int:animal_id>/', views.animal_detail, name='animal_detail'),
    path('<int:animal_id>/schedule/', views.animal_schedule, name='animal_schedule'),
    path('<int:animal_id>/feedback/', views.animal_feedback, name='animal_feedback'),
    path('<int:animal_id>/get_walk_form/', views.get_walk_form, name='get_walk_form'),
]
