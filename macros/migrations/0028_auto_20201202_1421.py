# Generated by Django 3.0 on 2020-12-02 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('macros', '0027_auto_20201202_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='current_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='macros.Profile'),
        ),
    ]
