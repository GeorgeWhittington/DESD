# Generated by Django 5.0.2 on 2024-05-02 00:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_appointments', '0024_alter_appointment_stage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='staff_preference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_preferred_staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prescriptionrequest',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prescriptionrequest',
            name='approved_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prescriptionrequest',
            name='requested_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]