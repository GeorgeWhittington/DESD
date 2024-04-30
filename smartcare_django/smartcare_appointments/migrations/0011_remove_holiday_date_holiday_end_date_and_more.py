# Generated by Django 5.0.2 on 2024-03-30 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_appointments', '0010_remove_workingday_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='holiday',
            name='date',
        ),
        migrations.AddField(
            model_name='holiday',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='holiday',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
