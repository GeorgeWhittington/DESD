from smartcare_auth.models import Staff
from smartcare_appointments.models import Appointment, TimeOff
from django.conf import settings
from datetime import datetime,date,timedelta
from django.db.models import Q


def scheduler(appointment):
    print("STARTED SCHEDULING")
    dateRequested = appointment.date_requested
    timeRequested = appointment.time_preference
    #returns the staff available on the requested date
    availableStaff = get_staff_working_on_date(dateRequested)

    print("AVAILABLE STAFF",availableStaff)

    for staff in availableStaff:
        availableSlot = staff_get_available_slot(staff,dateRequested,timeRequested)

        if availableSlot is not None:
            print("CHOSEN DETAILS: ", staff, availableSlot)
            appointmentScheduled = schedule_appointment(staff, availableSlot,appointment,dateRequested)
            if appointmentScheduled:
                ("APPOINTMENT SCHEDULED")
                return True
    
    return False


# schedule the appointment using the chosen staff and slot
def schedule_appointment(staff, slot, appointment,dateRequested):
    try:
        appointment.slot_number = slot
        slotStartTime = settings.SLOTS[slot]['start']
        convertedSlotTime = datetime.strptime(slotStartTime, '%H:%M:%S').time()
        appointment.staff = staff.user
        appointment.stage = 1
        appointment.assigned_start_time = (datetime.combine(dateRequested,convertedSlotTime)).isoformat()
        appointment.save()
        return True
    except Exception:
        return False


# handles appointments affected by unplanned leave: tries to reschedule
def handle_affected_appointments(affected_appointments):
    for appointment in affected_appointments:
        rescheduled = scheduler(appointment)
        if not rescheduled:
            print("APPOINTMENT ", appointment, " CANCELLED")
            appointment.stage = 3
            appointment.staff = None
            appointment.slot_number = -1
            appointment.assigned_start_time = None
            appointment.save()

# find the staff who are working on the chosen day and are not on time off
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

# get a staff's available slots 
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
        
    return availableSlotNumbers[0] if availableSlotNumbers else False
    
# gets a staff member's appointments
def staff_get_appointments(staff,date):

    staffHasAppointments = Appointment.objects.filter(
        staff = staff.user,
        assigned_start_time__date = date
    )

    appointmentSlotNumbers = {appointment.slot_number for appointment in staffHasAppointments}

    return appointmentSlotNumbers



def checkSlotsInRange(startDate,endDate):
    
    result = {}
    while startDate <= endDate:
        morningAvailable = False
        eveningAvailable = False
        availableStaff = get_staff_working_on_date(startDate)

        for staff in availableStaff:
            slots =[]
            morningSlot = staff_get_available_slot(staff,startDate,0)
            eveningSlot = staff_get_available_slot(staff,startDate,1)
            if morningSlot is not None and eveningSlot is not None:
                
                slots.append(morningSlot)
                slots.append(eveningSlot)
                for slot in slots:
                    slotStartTime = settings.SLOTS[slot]['start']
                    convertedSlotTime = datetime.strptime(slotStartTime, '%H:%M:%S').time()
                    eveningCutoffTime = datetime.strptime('12:00:00', '%H:%M:%S').time()
                    if convertedSlotTime <= eveningCutoffTime:
                        morningAvailable = True
                        
                    else:
                        eveningAvailable = True
                    date = startDate.strftime("%Y-%m-%d")
                    result[date] = [morningAvailable,eveningAvailable]

        
        startDate = startDate + timedelta(days=1)

    return result

print(checkSlotsInRange(datetime(2024, 4, 17),datetime(2024, 4, 30)))
 
    