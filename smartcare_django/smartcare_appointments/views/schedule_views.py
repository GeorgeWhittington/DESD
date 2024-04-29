from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import viewsets, mixins


from smartcare_appointments.models import TimeOff
from smartcare_appointments.schedule_serializers import TimeOffSerializer
from smartcare_auth.rest_permissions import IsStaff

class TimeOffView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):#viewsets.ModelViewSet
    queryset = TimeOff.objects.all()
    serializer_class = TimeOffSerializer

    permission_classes = [IsStaff]



    