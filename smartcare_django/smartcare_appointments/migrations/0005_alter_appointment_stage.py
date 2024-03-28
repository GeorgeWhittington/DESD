# Generated by Django 5.0.2 on 2024-03-28 12:15

import smartcare_appointments.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_appointments', '0004_appointment_symptom_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='stage',
            field=models.IntegerField(choices=[(0, 'REQUESTED'), (1, 'OPEN'), (2, 'COMPLETED'), (3, 'CANCELLED')], default=smartcare_appointments.models.AppointmentStage['REQUESTED']),
        ),
    ]