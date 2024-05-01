from datetime import datetime, date, timezone

from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from smartcare_appointments.models import Prescription, PrescriptionRequest
from smartcare_appointments.prescriptions_serializers import PrescriptionsSerializer, PrescriptionsRequestSerializer
from smartcare_auth.rest_permissions import IsStaff, IsStaffOrExternal


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

    '''
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStaff()]
        elif self.action == "create_request":
            return [permissions.IsAuthenticated()]
        else:
            return [IsStaffOrExternal()]
    '''
    @action(detail=False)
    def prescription_requests(self, request):
        pass
    
    #To do: @action(detail=False, methods=['post']) Make another action with repeat perscription serializer fo patients to create a new repeat prescription request
    @action(detail=False, methods=['post'])
    def create_request(self, request):
        user = request.user
        try:
            prescription_id = request.data.pop("prescription_id")
        except KeyError:
            return Response({"result" : False, "message": "could not locate prescription"}, status=status.HTTP_400_BAD_REQUEST)
        
        for i in prescription_id:
            prescription = Prescription.objects.get(pk=i)

            if user.is_clinic_staff():
                return Response({"result" : False, "message": "cannot create request for non patient user"})
            
            if not prescription:
                return Response({"result" : False, "message": "failed to get prescription"})

            print(prescription_id)
            
            prescription_request = PrescriptionRequest()
            prescription_request.prescription = prescription
            prescription_request.requested_time = datetime.now(timezone.utc)
            prescription_request.save()
        
        return Response({"result" : True, "message": "success"})

    #To do: @action(detail=False, methods=['post']) Make another action for doctors to be able to accept or reject prescription requests
    @action(detail=False, methods=['post'])
    def respond_request(self, request):
        user = request.user
        try:
            prescription_id = request.data.pop("prescription_id")
        except KeyError:
            return Response({"result" : False, "message": "could not locate prescription"}, status=status.HTTP_400_BAD_REQUEST)
        
        for i in prescription_id:
            prescription = Prescription.objects.get(pk=i)

            if not user.is_clinic_staff():
                return Response({"result" : False, "message": "only clinic staff can respond to prescription requests"})
            
            if not prescription:
                return Response({"result" : False, "message": "failed to get prescription"})
            
            print(prescription_id)
            
            prescription_request = PrescriptionRequest()
            prescription_request.approved_by = user
            prescription_request.approved_time = datetime.now(timezone.utc)
            
            prescription_request.save()
            
        

