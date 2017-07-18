from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Exercise(models.Model):
  EXERCISE_TYPES = (
    ('C', 'Cardio'),
    ('S', 'Strength'),
    ('O', 'Other'),
  )
  description = models.CharField(max_length=1000)
  exercise_type = models.CharField(max_length=1, choices=EXERCISE_TYPES, blank=True, null=True)

  def __unicode__(self):
      return str(self.description)

class SScore(models.Model):
  angry = models.FloatField()
  sad = models.FloatField()

  def __unicode__(self):
    feelings = [self.angry, self.sad]
    tags = ['angry', 'sad']
    text = ""
    for i in range(0, len(tags)):
      if feelings[i] >= 0.000:
        text += tags[i]+": "+str(feelings[i])+"\n"
    return text

class Entry(models.Model):
  user_name = models.CharField(max_length=2000)
  date = models.DateField()
  exercise = models.ForeignKey(Exercise, blank=True, null=True, on_delete=models.CASCADE)
  sleep = models.FloatField()
  meditation = models.BooleanField()
  meditation_time = models.FloatField(blank=True, null=True)
  mood = models.TextField()
  mood_number = models.IntegerField()
  score = models.ForeignKey(SScore, on_delete=models.CASCADE)

  def __unicode__(self):
      return str(self.date)

  def delete(self, using=None):
    if self.exercise:
        self.exercise.delete()
    if self.score:
        self.score.delete()
    super(Profile, self).delete(using)