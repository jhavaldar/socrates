# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-17 00:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0007_auto_20170715_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='art',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='calories',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='miles',
        ),
        migrations.RemoveField(
            model_name='sscore',
            name='calm',
        ),
        migrations.RemoveField(
            model_name='sscore',
            name='happy',
        ),
    ]
