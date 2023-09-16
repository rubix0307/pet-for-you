from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
]
