from django.conf import settings
from django.db import models
from smartcare_auth.models import User, Staff,EmploymentType
from enum import IntEnum


class WorkingDay(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='working_days')
    day = models.CharField(max_length=9, choices=settings.DAY_CHOICES)

    def __str__(self):
        return f"{self.get_day_display()}"
    
    class Meta:
        unique_together = ('staff', 'day')

class Holiday(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='holidays')
    date = models.DateField()

    def __str__(self):
        return f"{self.staff.user.full_name()} - {self.date}"
    

def update_working_days(staff):
    # Define which days are target days based on employment type
    if staff.employment_type == EmploymentType.FULL_TIME:
        target_days = settings.FULL_TIME_WORKING_DAYS
    elif staff.employment_type == EmploymentType.PART_TIME:
        target_days = settings.PART_TIME_WORKING_DAYS
    else:
        target_days = []

    staff.working_days.exclude(day__in=target_days).delete()
    
    for day in target_days:
        WorkingDay.objects.get_or_create(staff=staff, day=day)

def report_unavailability(start_date, end_date=None):
    pass

def calculate_available_slots(user, date):
    pass