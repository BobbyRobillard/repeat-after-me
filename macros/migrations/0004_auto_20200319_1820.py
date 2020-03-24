# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-03-19 22:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("macros", "0003_auto_20200319_1641")]

    operations = [
        migrations.AlterField(
            model_name="settings",
            name="current_profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="macros.Profile",
            ),
        )
    ]
