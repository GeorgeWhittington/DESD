# Generated by Django 5.0.2 on 2024-04-29 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartcare_finance', '0005_remove_invoice_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='pay_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'PRIVATE'), (1, 'NHS')], default=0),
        ),
    ]
