from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from smartcare_appointments.models import AppointmentStage, Appointment, AppointmentComment
from smartcare_auth.models import UserType
from smartcare_auth.serializers import UserSerializer, BasicUserSerializer

UserModel = get_user_model()


class AppointmentCommentSerializer(serializers.ModelSerializer):
    created_by = BasicUserSerializer(read_only=True)

    def create(self, validated_data):
        appointment_id = validated_data["appointment_id"]
        appointment = Appointment.objects.get(pk=appointment_id)
        text = validated_data["text"]

        if appointment is not None:
            comment = AppointmentComment.objects.create(
                appointment=appointment,
                text=text
            )
            comment.save()
            return comment

    class Meta:
        model = AppointmentComment
        fields = ['id', 'created_by', 'created_time', 'text']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    staff = BasicUserSerializer(read_only=True, required=False)
    staff_preference = BasicUserSerializer(read_only=True, required=False)
    staff_preference_id = serializers.IntegerField(write_only=True, required=False)
    appointment_comments = AppointmentCommentSerializer(many=True, read_only=True)

    def create(self, validated_data):
        if self.context["request"].user.user_type != UserType.PATIENT:
            raise ValidationError({"patient": "Only patient accounts can request appointments"})

        symptoms = validated_data["symptoms"]
        time_preference = validated_data["time_preference"]
        symptom_duration = validated_data["symptom_duration"]
        date_requested = validated_data["date_requested"]
        staff_preference = None

        staff_preference_id = validated_data.get("staff_preference_id")
        if staff_preference_id is not None:
            staff_preference = UserModel.objects.filter(pk=staff_preference_id, user_type__in=[UserType.DOCTOR, UserType.NURSE]).first()

        appointment = Appointment.objects.create(
            patient=self.context['request'].user,
            symptoms=symptoms,
            stage=AppointmentStage.REQUESTED,
            time_preference=time_preference,
            staff_preference=staff_preference,
            symptom_duration=symptom_duration,
            date_requested=date_requested
        )
        appointment.save()

        comment = AppointmentComment.objects.create(
            created_by=appointment.patient,
            appointment=appointment,
            text="Appointment requested"
        )
        comment.save()

        return appointment

    class Meta:
        model = Appointment
        fields = ["id", "patient", "staff", "date_created", "symptoms", "stage", "symptom_duration",
                  "time_preference", "staff_preference", "staff_preference_id", "slot_number", "assigned_start_time",
                  "actual_start_time", "actual_end_time", "date_requested", "appointment_comments"]
        extra_kwargs = {
            "staff": {
                "required": False
            }
        }
