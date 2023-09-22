import datetime as dt
from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title','text','media',]


class PetWalkForm(forms.Form):
    date = forms.DateField(
        label='День',
        widget=forms.DateInput(
            attrs={
                'type':'date',
                'value':dt.datetime.now().strftime('%Y-%m-%d'),
                'min':dt.datetime.now().strftime('%Y-%m-%d'),
                'max':(dt.datetime.now()+dt.timedelta(weeks=4)).strftime('%Y-%m-%d'),
                'id':"id_date",
            }),
        required=True
    )
    duration = forms.IntegerField(
        label='Продолжительность (мин)',
        min_value=15,
        initial=15,
        widget=forms.NumberInput(
            attrs={
                'min': 15,
                'step': 15,
                'id':'id_duration',
            }),
        required=True
    )
    start_in = forms.ChoiceField(
        label='Начало прогулки:',
        choices=[],
        widget=forms.Select(),
        required=True
    )