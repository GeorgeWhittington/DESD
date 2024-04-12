from rest_framework import serializers

from smartcare_appointments.models import AppointmentStage, Appointment, AppointmentComment, TimeOff
from smartcare_auth.serializers import UserSerializer


class AppointmentCommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = AppointmentComment
        fields = ['id', 'created_by', 'created_time', 'text']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    staff = UserSerializer(read_only=True, required=False)
    appointment_comments = AppointmentCommentSerializer(many=True, read_only=True)
    def create(self, validated_data):
        symptoms = validated_data["symptoms"]
        time_preference = validated_data["time_preference"]
        symptom_duration = validated_data["symptom_duration"]
        date_requested = validated_data["date_requested"]

        appointment = Appointment.objects.create(
            patient=self.context['request'].user,
            symptoms=symptoms,
            stage=AppointmentStage.REQUESTED,
            time_preference=time_preference,
            symptom_duration=symptom_duration,
            date_requested=date_requested
        )
        appointment.save()

        return appointment

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'staff', 'symptoms', 'stage', 'symptom_duration', 'time_preference', 'assigned_start_time', 'actual_start_time', 'actual_end_time', 'date_requested', 'appointment_comments']
        extra_kwargs = {
            "staff": {
                "required": False
            }
        }
