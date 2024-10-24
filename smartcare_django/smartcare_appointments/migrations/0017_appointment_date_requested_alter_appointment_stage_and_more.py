# Generated by Django 5.0.2 on 2024-04-04 16:07

import django.utils.timezone
import smartcare_appointments.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_appointments', '0016_rename_reason_appointment_symptoms'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='date_requested',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='stage',
            field=models.IntegerField(choices=[(0, 'REQUESTED'), (1, 'SCHEDULED'), (2, 'COMPLETED'), (3, 'CANCELLED')], default=smartcare_appointments.models.AppointmentStage['REQUESTED']),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='symptoms',
            field=models.TextField(blank=True, default=''),
        ),
    ]
