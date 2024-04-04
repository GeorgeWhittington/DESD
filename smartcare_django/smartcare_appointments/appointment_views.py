from rest_framework.views import APIView
from rest_framework import routers, serializers, viewsets, generics, permissions
from rest_framework.renderers import JSONRenderer
from smartcare_appointments.models import Appointment
from smartcare_appointments.serializers import AppointmentSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

class AppointmentView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        appointment = self.get_object()
        return Response({"result" : f"request to approve {appointment.id}"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        appointment = self.get_object()
        return Response({"result" : "success"})