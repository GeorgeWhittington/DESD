# Generated by Django 5.0.2 on 2024-03-27 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_auth', '0009_alter_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='employment_type',
            field=models.CharField(blank=True, choices=[('FT', 'Full Time'), ('PT', 'Part Time')], max_length=2, null=True),
        ),
    ]