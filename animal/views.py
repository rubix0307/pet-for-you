from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from .models import Animal, Sex
# Create your views here.

def animal_index(request: WSGIRequest):
    context = dict()

    animals = Animal.objects.order_by('-id').all()

    context.update(dict(
        animals=animals,
    ))

    return render(request, 'animal/index.html', context=context)