from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Exercise(models.Model):
  EXERCISE_TYPES = (
    ('C', 'Cardio'),
    ('S', 'Strength'),
    ('O', 'Other'),
  )
  miles = models.FloatField(blank=True, null=True)
  description = models.CharField(max_length=1000)
  exercise_type = models.CharField(max_length=1, choices=EXERCISE_TYPES, blank=True, null=True)

  def __unicode__(self):
      return self.description

class Entry(models.Model):
  date = models.DateField()
  exercise = models.ForeignKey(Exercise, blank=True, null=True)
  calories = models.IntegerField()
  sleep = models.FloatField()
  art = models.IntegerField()
  meditation = models.BooleanField()
  meditation_time = models.FloatField(blank=True, null=True)
  mood = models.TextField()
  mood_number = models.IntegerField()

  def __unicode__(self):
      return self.date