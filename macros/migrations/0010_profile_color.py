# Generated by Django 3.0 on 2020-03-29 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("macros", "0009_auto_20200327_1427")]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="color",
            field=models.CharField(default="000000", max_length=7),
            preserve_default=False,
        )
    ]
