from datetime import datetime, date, timezone

from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from smartcare_appointments.models import Prescription, PrescriptionRequest
from smartcare_appointments.prescriptions_serializers import PrescriptionsSerializer, PrescriptionsRequestSerializer
from smartcare_auth.rest_permissions import IsStaff, IsStaffOrExternal, IsAuthenticatedAndNotExternal, PrescriptionRequestIsOwnerOrStaffOrExternal
from smartcare_auth.models import User

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
    
    @action(detail=False, methods=['post'])
    def create_prescription(self, request):
        user = request.user
        try:
            patient_id = request.data.pop("patient_id")
            medicine = request.data.pop("medicine")
            notes = request.data.pop("notes")
            is_repeating = request.data.pop("is_repeating")
        except KeyError:
            return Response({"result" : False, "message": "could not locate required data"}, status=status.HTTP_400_BAD_REQUEST)
       
        patient = User.objects.filter(pk__in=patient_id).first()

        if not patient :
            return Response({"result" : False, "message": "no valid patient ids provided"}, status=status.HTTP_400_BAD_REQUEST)

        prescription = Prescription()
        prescription.medicine = medicine
        prescription.notes = notes
        prescription.is_repeating = is_repeating
        prescription.patient = patient
        prescription.staff = user
        prescription.save()

        return Response({"result" : True, "message": f"success, prescription for {patient.username} was created"}, status=status.HTTP_200_OK)
    


class PrescriptionRequestView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PrescriptionRequest.objects.all()
    serializer_class = PrescriptionsRequestSerializer

    def get_permissions(self):
        if self.action == "create_request":
            return [IsAuthenticatedAndNotExternal()]
        elif self.action == "respond_request":
            return [IsStaff()]
        else:
            return [PrescriptionRequestIsOwnerOrStaffOrExternal()]
    
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

            
            prescription_request = PrescriptionRequest()
            prescription_request.prescription = prescription
            prescription_request.requested_time = datetime.now(timezone.utc)
            prescription_request.save()
        
        return Response({"result" : True, "message": "success"})

    @action(detail=False, methods=['post'])
    def respond_request(self, request):
        user = request.user
        prescription_request_ids = request.data.get("prescription_request_ids")
        is_approved = request.data.get("is_approved")
        
        if prescription_request_ids is None or not isinstance(prescription_request_ids, list) or len(prescription_request_ids) == 0:
            return Response({"result" : False, "message": "could not locate prescription_request_ids"}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_approved is None:
            return Response({"result" : False, "message": "not approving or rejecting request, please set is_approved"}, status=status.HTTP_400_BAD_REQUEST)

        prescription_requests = PrescriptionRequest.objects.filter(pk__in=prescription_request_ids).all()

        if len(prescription_requests) == 0:
            return Response({"result" : False, "message": "no valid prescription request ids provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        for prescription_request in prescription_requests:
            prescription_request.approved_by = user
            prescription_request.approved_time = datetime.now(timezone.utc)
            prescription_request.save()

        return Response({"result" : True, "message": f"success, {len(prescription_requests)} were updated"}, status=status.HTTP_200_OK)
        

