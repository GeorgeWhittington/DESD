from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

from smartcare_appointments.models import Prescription, PrescriptionRequest
from smartcare_appointments.serializers import PrescriptionsSerializer

class PrescriptionsView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionsSerializer