from rest_framework import serializers
from smartcare_appointments.schedule_models import TimeOff, WorkingDay


class TimeOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeOff
        fields = ['staff', 'start_date', 'end_date', 'reason']


class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDay
        fields = ['day']