# Generated by Django 3.0 on 2020-03-27 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("macros", "0008_keyevent_order_in_recording")]

    operations = [
        migrations.AlterField(
            model_name="keyevent",
            name="order_in_recording",
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name="mouseevent",
            name="order_in_recording",
            field=models.IntegerField(default=-1),
        ),
    ]
