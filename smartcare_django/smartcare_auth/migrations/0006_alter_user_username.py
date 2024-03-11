# Generated by Django 5.0.2 on 2024-03-02 19:32

import smartcare_auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_auth', '0005_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and ./+/-/_ only.', max_length=150, unique=True, validators=[smartcare_auth.validators.UnicodeNoEmailUsernameValidator()], verbose_name='username'),
        ),
    ]