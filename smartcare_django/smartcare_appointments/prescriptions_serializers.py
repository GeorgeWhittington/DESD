from rest_framework import serializers

from smartcare_appointments.models import Prescription, PrescriptionRequest
from smartcare_auth.serializers import UserSerializer

class PrescriptionsSerializer(serializers.HyperlinkedModelSerializer):
    patient = UserSerializer(read_only=True)
    staff = UserSerializer(read_only=True)
    class Meta:
        model = Prescription
        fields = ['id', 'appointment', 'medicine', 'notes', 'is_repeating', 'patient', 'staff']
        extra_kwargs = {
            "staff": {
                "required": False
            }
        }
    
class PrescriptionsRequestSerializer(serializers.HyperlinkedModelSerializer):
    prescription = PrescriptionsSerializer(read_only =True)
    patient = UserSerializer(read_only=True)
    staff = UserSerializer(read_only=True)
    class Meta:
        model = PrescriptionRequest
        fields = ['id', 'requested_time', 'approved_time', 'collected', 'staff', 'patient', 'prescription']
        extra_kwargs = {
            "staff": {
                "required": False
            }
        }
    