from rest_framework import serializers

from smartcare_appointments.models import Prescription, PrescriptionRequest
from smartcare_auth.serializers import UserSerializer

class PrescriptionsSerializer(serializers.HyperlinkedModelSerializer):
    patient = UserSerializer(read_only=True)
    staff = UserSerializer(read_only=True)
    #first_name = serializers.Field(source='smartcare_auth_user.first_name')
    #last_name = serializers.Field(source='smartcare_auth_user.last_name')
    class Meta:
        model = Prescription
        fields = ['id', 'appointment', 'medicine', 'notes', 'is_repeating', 'patient', 'staff']
        extra_kwargs = {
            "staff": {
                "required": False
            }
        }

''' Don't need this
class PatientsSerializer(serializers.HyperlinkedModelSerializer):
    prescriptions = PrescriptionsSerializer(many=True, read_only=True)
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'prescriptions']
        extra_kwargs = {
            "staff": {
                "required": False
            }
        }
'''