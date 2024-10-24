# Generated by Django 5.0.2 on 2024-03-25 11:57

import smartcare_appointments.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='stage',
            field=models.IntegerField(choices=[(0, 'REQUESTED'), (1, 'OPEN'), (2, 'COMPLETED')], default=smartcare_appointments.models.AppointmentStage['REQUESTED']),
        ),
    ]
