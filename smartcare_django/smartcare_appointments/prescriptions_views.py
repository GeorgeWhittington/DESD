from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from smartcare_appointments.prescriptions_models import Prescription, PrescriptionRequest
from smartcare_appointments.prescriptions_serializers import PrescriptionsSerializer, PrescriptionsRequestSerializer


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_clinic_staff()


class IsStaffOrExternal(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_clinic_or_external_staff()


class PrescriptionsView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionsSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStaff()]
        elif self.action == "my_prescriptions":
            return [permissions.IsAuthenticated()]
        else:
            return [IsStaffOrExternal()]
        
    @action(detail=False)
    def my_prescriptions(self, request):
        queryset = Prescription.objects.filter(patient=request.user)
        serializer = PrescriptionsSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    #To do: Make another action for archiving prescriptions



    #To do: Make prescriptionsrequests view

class PrescriptionRequestView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PrescriptionRequest.objects.all()
    serializer_class = PrescriptionsRequestSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStaff()]
        elif self.action == "createPrescriptionRequest":
            return [permissions.IsAuthenticated()]
        else:
            return [IsStaffOrExternal()]

    #To do: @action(detail=False, methods=['post']) Make another action with repeat perscription serializer fo patients to create a new repeat prescription request
    @action(detail=False, methods=['post'])
    def createPrescriptionRequest(self, request):
        queryset = PrescriptionRequest.objects.filter(patient=request.user)
        serializer = PrescriptionsRequestSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    #To do: @action(detail=False, methods=['post']) Make another action for doctors to be able to accept or reject prescription requests