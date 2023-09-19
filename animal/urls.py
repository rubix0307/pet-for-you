from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.animal_index, name='animal_index'),
]
