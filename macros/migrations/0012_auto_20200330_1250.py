# Generated by Django 3.0 on 2020-03-30 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("macros", "0011_auto_20200329_0634")]

    operations = [
        migrations.RenameField(
            model_name="profile", old_name="color_code", new_name="color"
        )
    ]
