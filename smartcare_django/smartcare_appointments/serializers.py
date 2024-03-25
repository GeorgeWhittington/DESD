from rest_framework import serializers

from smartcare_appointments.models import AppointmentStage, Appointment
from smartcare_auth.serializers import UserSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    staff = UserSerializer(read_only=True, required=False)

    def create(self, validated_data):
        reason = validated_data["reason"]
        time_slot = validated_data["time_slot"]

        appointment = Appointment.objects.create(
            patient=self.context['request'].user,
            reason=reason,
            stage=AppointmentStage.REQUESTED,
            time_slot=time_slot
        )
        appointment.save()

        return appointment

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'staff', 'reason', 'stage', 'time_slot', 'assigned_start_time', 'actual_start_time', 'actual_end_time']
        extra_kwargs = {
            "staff": {
                "required": False
            }
        }