# Generated by Django 3.0 on 2020-04-07 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("macros", "0018_auto_20200403_1920")]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="offer_tutorial",
            field=models.BooleanField(default=True),
        )
    ]
