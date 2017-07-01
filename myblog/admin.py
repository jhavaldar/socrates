from django.contrib import admin
from django import forms

from myblog.models import Exercise, Entry

# Register your models here.

admin.site.register(Exercise)
admin.site.register(Entry)