from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest


def blog_index(request: WSGIRequest):
    return render(request, 'blog/index.html')