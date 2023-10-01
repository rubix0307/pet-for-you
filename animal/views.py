import datetime as dt
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from .models import Animal, Sex, Feedback
from .forms import PetWalkForm, FeedbackForm
from .utils import get_available_pet_walk_time


def animal_index(request: WSGIRequest):
    animals = Animal.objects.order_by('-id').all()

    context = dict(
        animals=animals,
    )

    return render(request, 'animal/index.html', context=context)

def get_walk_form(request: WSGIRequest, animal=None, only_form=False):

    initial_values = dict(
        date=request.POST.get('date', dt.datetime.now().strftime('%Y-%m-%d')),
        duration=int(request.POST.get('duration', 15)),
        start_in=request.POST.get('start_in', None)
    )
    walk_times = [(dt.datetime(year=2023, month=9, day=23, hour=9, minute=15), dt.datetime(year=2023, month=9, day=23, hour=9, minute=30))]

    start_in = get_available_pet_walk_time(
        selected_day=dt.datetime.strptime(initial_values['date'], '%Y-%m-%d'),
        walk_times=walk_times,
        duration=initial_values['duration'],
    )

    walk_form = PetWalkForm(initial=initial_values)
    walk_form.fields['start_in'].choices = [(i, i) for i in start_in]
    walk_form.fields['start_in'].label += f'''<div>Мест: {len(walk_form.fields['start_in'].choices)}</div>'''

    if only_form:
        return walk_form
    return render(request, 'animal/inc/_walk-form.html', context=dict(walk_form=walk_form))

def animal_detail(request: WSGIRequest, animal_id):

    animal = Animal.objects.get(id=animal_id)
    feedbacks = Feedback.objects.filter(animal=animal)
    context = dict(
        animal=animal,
        walk_form=get_walk_form(request, animal, only_form=True),
        feedback_form=FeedbackForm(),
        feedbacks=feedbacks,
    )

    return render(request, 'animal/detail.html', context=context)

def animal_schedule(request: WSGIRequest, animal_id):
    return redirect('animal_detail', animal_id=animal_id)

def animal_feedback(request: WSGIRequest, animal_id):
    post_data = dict(
        encoding=request.POST.get('encoding'),
        csrfmiddlewaretoken=request.POST.get('csrfmiddlewaretoken'),
        title=request.POST.get('title'),
        text=request.POST.get('text'),
        user=request.user,
        animal=Animal.objects.filter(id=animal_id).first(),
    )

    form = FeedbackForm(post_data)
    if form.is_valid():
        form.save()

    return redirect('animal_detail', animal_id=animal_id)
