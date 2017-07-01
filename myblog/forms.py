from django import forms

from .models import Entry, Exercise

EXERCISE_TYPES = (
  ('C', 'Cardio'),
  ('S', 'Strength'),
  ('O', 'Other'),
)

class PostForm(forms.Form):
    did_exercise = forms.BooleanField(initial=False, required=False)
    exercise_type = forms.ChoiceField(choices=EXERCISE_TYPES, required=False,initial='O')
    exercise_description = forms.CharField(required=True, initial="Brief description of exercise.")
    miles = forms.FloatField(required=False, initial=0.0)
    calories = forms.IntegerField(required=True,initial=2000)
    sleep = forms.FloatField(required=True,initial=8.0)
    art = forms.IntegerField(required=True, initial=3)
    meditation = forms.BooleanField(initial=False, required=False)
    mood = forms.CharField(required=True, initial="How are you feeling today?")
    mood_number = forms.IntegerField(required=True, initial=3)
    meditation_time = forms.FloatField(required=False)

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
