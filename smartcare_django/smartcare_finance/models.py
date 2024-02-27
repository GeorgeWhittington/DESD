from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator

# ASK ABOUT PAYMENTS
class Invoice(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])
    is_paid = models.BooleanField(default=False)
    creation_time = models.DateTimeField(null=True)
