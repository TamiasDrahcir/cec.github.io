# Generated by Django 5.1 on 2024-10-28 07:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cec', '0003_remove_survey_deadline_survey_opening_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2099, 12, 31, 0, 0)),
        ),
    ]
