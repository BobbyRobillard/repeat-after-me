# Generated by Django 3.0 on 2020-04-09 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('macros', '0020_settings_show_social_sharing'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='quick_play_key',
            field=models.CharField(default='q', max_length=10),
            preserve_default=False,
        ),
    ]
