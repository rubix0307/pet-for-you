import datetime as dt
from dataclasses import dataclass
import pytz
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from .models import Animal, Sex, Feedback, Schedule
from .forms import PetWalkForm, FeedbackForm
from .utils import get_available_pet_walk_time


def animal_index(request: WSGIRequest):
    animals = Animal.objects.order_by('-id').all()

    context = dict(
        animals=animals,
    )

    return render(request, 'animal/index.html', context=context)

@dataclass
class WalkFormInitialValues:
    date: str
    duration: int
    start_in: str | None

    def __post_init__(self):
        if isinstance(self.duration, str):
            self.duration = int(self.duration)


def get_walk_form(request: WSGIRequest, animal=None, animal_id=None, initial_values:WalkFormInitialValues=None, only_form=False):
    if not animal and animal_id:
        animal = Animal.objects.filter(id=animal_id).first()

    if not initial_values:
        initial_values = WalkFormInitialValues(
            date=request.POST.get('date', dt.datetime.now().strftime('%Y-%m-%d')),
            duration=int(request.POST.get('duration', 15)),
            start_in=request.POST.get('start_in', None)
        )
    walk_times = Schedule.objects.filter(animal=animal).all()
    start_in = get_available_pet_walk_time(
        selected_day=initial_values.date,
        walk_times=list(walk_times),
        duration=initial_values.duration,
    )

    walk_form = PetWalkForm(initial=initial_values.__dict__)
    walk_form.fields['start_in'].choices = [(i, i) for i in start_in]
    walk_form.fields['start_in'].label += f'''<div>Мест: {len(walk_form.fields['start_in'].choices)}</div>'''

    if only_form:
        return walk_form
    return render(request, 'animal/inc/_walk-form.html', context=dict(walk_form=walk_form, animal=animal))

def animal_detail(request: WSGIRequest, animal_id):

    animal = Animal.objects.get(id=animal_id)
    feedbacks = Feedback.objects.filter(animal=animal)

    today = dt.date.today()
    walk_times = Schedule.objects.filter(
        Q(start_time__date__gte=today),
        animal=animal,
        user=request.user
    ).order_by('start_time').all()

    context = dict(
        animal=animal,
        walk_form=get_walk_form(request, animal, only_form=True),
        feedback_form=FeedbackForm(),
        feedbacks=feedbacks,
        walk_times=walk_times,
    )

    return render(request, 'animal/detail.html', context=context)

def animal_schedule(request: WSGIRequest, animal_id):
    if request.method == 'POST':
        animal = Animal.objects.filter(id=animal_id).first()

        selected_day = request.POST.get('date')
        duration = int(request.POST.get('duration'))
        try:
            start_in = dt.datetime.strptime(request.POST.get('start_in',''), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            messages.error(request, 'Не указано время начала прогулки')
            return redirect('animal_detail', animal_id=animal_id)

        walk_times = Schedule.objects.filter(animal=animal).all()

        available_times = get_available_pet_walk_time(
            selected_day=selected_day,
            walk_times=walk_times,
            duration=duration,
        )

        if start_in in available_times:
            end_time = (start_in + dt.timedelta(minutes=duration))

            schedule_entry = Schedule(
                start_time=start_in.replace(tzinfo=pytz.utc),
                end_time=end_time.replace(tzinfo=pytz.utc),
                animal=animal,
                user=request.user,
            )
            schedule_entry.save()
        else:
            messages.error(request, 'Выбранное время, уже занято')

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
