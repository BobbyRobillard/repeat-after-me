# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-03-21 23:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('macros', '0006_auto_20200320_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='updates_waiting',
            field=models.BooleanField(default=False),
        ),
    ]