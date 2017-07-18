from django import forms
import sys
from .models import Entry, Exercise

EXERCISE_TYPES = (
  ('C', 'Cardio'),
  ('S', 'Strength'),
  ('O', 'Other'),
)

class PostForm(forms.Form):
    did_exercise = forms.BooleanField(initial=False, required=False)
    exercise_type = forms.ChoiceField(choices=EXERCISE_TYPES, required=False,initial='O')
    exercise_description = forms.CharField(required=False, initial="Brief description of exercise.")
    sleep = forms.FloatField(required=True,initial=8.0)
    meditation = forms.BooleanField(initial=False, required=False)
    mood = forms.CharField(required=True, initial="How are you feeling today?", widget=forms.Textarea(attrs={'cols': 40, 'rows': 20}))
    mood_number = forms.IntegerField(required=False, initial=3)
    meditation_time = forms.FloatField(required=False)

