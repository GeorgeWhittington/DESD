# Generated by Django 5.0.2 on 2024-04-29 17:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_appointments', '0023_alter_appointment_date_created'),
        ('smartcare_auth', '0017_passwordreset'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientInfo',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='patient_info', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('pay_type', models.PositiveSmallIntegerField(choices=[(0, 'PRIVATE'), (1, 'NHS')], default=0)),
            ],
        ),
        migrations.RenameModel(
            old_name='Staff',
            new_name='StaffInfo',
        ),
    ]
