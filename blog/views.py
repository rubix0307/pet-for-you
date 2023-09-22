from django.shortcuts import render
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from .models import Blog, Tag


def blog_index(request: WSGIRequest):
    context = dict()
    tag_name = request.GET.get('tag')

    posts = Blog.objects.order_by('-id')
    try:
        if tag_name:
            tag = Tag.objects.get(name=tag_name)
            posts = posts.filter(tag=tag)
            context.update(dict(is_tag=True))
    except Tag.DoesNotExist:
        messages.error(request, 'Искомый тег не существует')

    finally:
        posts = posts.all()
        tags = Tag.objects.filter(blog__isnull=False).distinct()
        context.update(dict(
            posts=posts,
            tags=tags,
        ))

    return render(request, 'blog/index.html', context=context)