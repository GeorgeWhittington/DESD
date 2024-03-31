from smartcare_auth.models import Staff

#Then test the appointments they already have for that date against the slots they are working: (test the appointment model for any appointments that match the staff)
#import appointment model
#list = Appoimtment.get_all().filter



def calculate_available_slots(user, date):
    pass

def find_available_staff(date):
    day_of_week = date.strftime("%A")
    
    # Start with all staff scheduled to work on that day of the week
    available_staff = Staff.objects.filter(
        working_days__day=day_of_week
    )
    
    # Exclude staff who have time off on that date
    available_staff = available_staff.exclude(
        time_off__date=date
    )
    
    # Exclude staff who already have appointments at any slot for that date
    available_staff = available_staff.exclude(
        appointments__date=date
    )
    
    return available_staff