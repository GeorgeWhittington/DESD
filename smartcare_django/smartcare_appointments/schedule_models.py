from django.conf import settings
from django.db import models
from smartcare_auth.models import User
from enum import IntEnum



class NonWorkingDays(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    

def update_working_days(user):
    pass

def report_unavailability(start_date, end_date=None):
    pass

def calculate_available_slots(user, date):
    pass