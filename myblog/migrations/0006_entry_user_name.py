# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-01 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0005_auto_20170701_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='user_name',
            field=models.CharField(default='admin', max_length=2000),
            preserve_default=False,
        ),
    ]
