from smartcare_auth.models import Staff
from smartcare_appointments.models import Appointment
from django.conf import settings
from datetime import datetime
from django.db.models import Q
from smartcare_appointments.schedule_models import TimeOff

#Then test the appointments they already have for that date against the slots they are working: (test the appointment model for any appointments that match the staff)
#import appointment model
#list = Appoimtment.get_all().filter



def calculate_available_slots(user, date):
    pass




# function which takes date,staff -> returns bool of if staff is free or not
# function to get the free slot which takes(time preference) and returns a slot

# def doctor_has_slot(staff,date):
#     slots = len(settings.SLOTS)
#     bookedAppointments = 




def schedule_appointment(appointment):
    print("TEST")
    date = appointment.date_requested
    timeRequested = appointment.time_preference

    print("time preference", timeRequested)
    
    availableStaff = get_staff_working_on_date(date)
    print("AVAILABLE STAFF",availableStaff)
    for staff in availableStaff:
        print(staff)
        #check if slot is available
            #slot = Invalid slot
            # check staff appointments
                #return appointments
            # for each alot check if available (start loop at preference)


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
    slot = settings.SLOT_INVALID

    slots = staff_get_appointments()
    for slot in slots:
        #if free
            return slot
    
def staff_get_appointments(staff,date):
    #search appointments
    pass
    #return   
    