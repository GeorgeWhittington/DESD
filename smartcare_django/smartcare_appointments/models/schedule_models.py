from django.conf import settings
from django.db import models
from smartcare_auth.models import StaffInfo



class WorkingDay(models.Model):
    staff = models.ForeignKey(StaffInfo, on_delete=models.CASCADE, related_name='working_days')
    day = models.CharField(max_length=9, choices=settings.DAY_CHOICES)

    def __str__(self):
        return f"{self.get_day_display()}"

    class Meta:
        unique_together = ('staff', 'day')


class TimeOff(models.Model):
    staff = models.ForeignKey(StaffInfo, on_delete=models.CASCADE, related_name='timeOff')
    start_date = models.DateField(blank= False, null= True)
    end_date = models.DateField(blank= False, null= True)
    reason = models.CharField(max_length=100, blank=True, default= 'Holiday')

    def __str__(self):
        return f"{self.staff.user.full_name()} - from {self.start_date} to {self.end_date}"

    class Meta:
        unique_together = ('staff', 'start_date','end_date')

