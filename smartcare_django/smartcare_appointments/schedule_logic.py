from smartcare_appointments.models import Appointment, TimeOff, WorkingDay
from smartcare_auth.models import Staff, EmploymentType
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from smartcare_appointments.slot_logic import handle_affected_appointments

# a doctor/nurse working days set by full time/part time defaults or by admin
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

def report_holiday(staff, start_date, end_date=None):
    if not end_date:
        end_date = start_date
    
    # Create the Holiday instance for the period of unavailability
    TimeOff.objects.create(staff=staff, start_date=start_date, end_date=end_date)

# unplanned leave
def report_unavailability(staff, start_date, end_date=None):
    if not end_date:
        end_date = start_date
    
    
    #TimeOff.objects.create(staff=staff, start_date=start_date, end_date=end_date)
    
    # Find appointments that overlap with the unavailability period
    affected_appointments = Appointment.objects.filter(
        staff=staff.user,
        assigned_start_time__range=(start_date, end_date)
    )
    
    if affected_appointments.exists():
        print("AFFECTED APPPOINTMENTS: ", affected_appointments)
        handle_affected_appointments(affected_appointments)

@receiver(post_save, sender=TimeOff)
def handle_unplanned_leave(sender, instance, created, **kwargs):
    if created and instance.reason == 'Unplanned leave':
        report_unavailability(instance.staff,instance.start_date, instance.end_date)