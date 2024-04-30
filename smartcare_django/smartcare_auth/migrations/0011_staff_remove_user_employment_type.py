# Generated by Django 5.0.2 on 2024-03-29 02:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_auth', '0010_user_employment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='staff_info', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('employment_type', models.CharField(blank=True, choices=[('FT', 'Full Time'), ('PT', 'Part Time')], max_length=2, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='employment_type',
        ),
    ]
