# Generated by Django 3.1.3 on 2020-12-07 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0006_auto_20201121_1032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rainfall',
            old_name='rainfall_last_day',
            new_name='rainfall',
        ),
        migrations.RemoveField(
            model_name='rainfall',
            name='rainfall_from_morning',
        ),
    ]
