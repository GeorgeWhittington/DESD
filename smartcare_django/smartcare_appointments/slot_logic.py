from smartcare_auth.models import Staff
from smartcare_appointments.models import Appointment, TimeOff
from django.conf import settings
from datetime import datetime,date
from django.db.models import Q


def scheduler(appointment):
    print("STARTED SCHEDULING")
    date = appointment.date_requested
    timeRequested = appointment.time_preference

    #returns the staff available on the requested date
    availableStaff = get_staff_working_on_date(date)

    print("AVAILABLE STAFF",availableStaff)

    for staff in availableStaff:

        availableSlot = staff_get_available_slot(staff,date,timeRequested)
        if availableSlot:
            schedule_appointment(staff, availableSlot)
            break


def schedule_appointment(staff, slot):
    pass

def get_staff_working_on_date(date):
    dateToDay = date.strftime("%A")
    print("Query Date:", date)
    print("Day of Week:", dateToDay)

    conflicting_holidays = TimeOff.objects.filter(start_date__lte=date, end_date__gte=date).only("id").all()
    print(f"conflicting holiday: {conflicting_holidays}")

    availableStaff = Staff.objects.filter(
        working_days__day=dateToDay
    ).exclude(
        timeOff__id__in=conflicting_holidays
    )
    print("AVAILABLE STAFF: ", availableStaff)
    return availableStaff

def staff_get_available_slot(staff,date,timePreference):
    
    # gets the appointments a doctor already has for date
    appointmentSlotNumbers = staff_get_appointments(staff,date)
    
    #stores available slots
    availableSlotNumbers = []

    
    if len(appointmentSlotNumbers) >= len(settings.SLOTS)-4:
        return False
    else:
        for slot in settings.SLOTS:
            if slot in settings.BREAK_SLOTS:
                continue
            elif slot in appointmentSlotNumbers:
                continue
            else:
                availableSlotNumbers.append(slot)

    if timePreference != 0:
        availableSlotNumbers = list(reversed(availableSlotNumbers))

    print(availableSlotNumbers)
        
    return availableSlotNumbers[0] if availableSlotNumbers else False
    
def staff_get_appointments(staff,date):

    staffHasAppointments = Appointment.objects.filter(
        staff = staff.user,
        assigned_start_time__date = date
    )

    appointmentSlotNumbers = {appointment.slot_number for appointment in staffHasAppointments}

    return appointmentSlotNumbers
 
    