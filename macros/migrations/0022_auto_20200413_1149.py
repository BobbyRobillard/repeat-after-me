# Generated by Django 3.0 on 2020-04-13 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('macros', '0021_settings_quick_play_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='play_mode_key',
            field=models.CharField(default='p', max_length=10),
        ),
        migrations.AlterField(
            model_name='settings',
            name='quick_play_key',
            field=models.CharField(default='a', max_length=10),
        ),
        migrations.AlterField(
            model_name='settings',
            name='recording_key',
            field=models.CharField(default='r', max_length=10),
        ),
    ]
