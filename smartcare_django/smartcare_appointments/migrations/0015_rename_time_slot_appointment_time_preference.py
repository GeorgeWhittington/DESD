# Generated by Django 5.0.2 on 2024-04-04 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_appointments', '0014_alter_timeoff_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='time_slot',
            new_name='time_preference',
        ),
    ]
