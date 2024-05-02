from datetime import timedelta

from django.utils.translation import ngettext
from django.contrib.auth import get_user_model, tokens
from rest_framework import permissions, viewsets, mixins, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from knox.views import LoginView as KnoxLoginView

from smartcare_auth.rest_permissions import IsStaff, IsAdmin, IsOwnerOrReadOnly
from smartcare_auth.models import StaffInfo, PasswordReset, UserType, EmploymentType, PayRate, PatientPayType
from smartcare_auth.serializers import UserSerializer, StaffSerializer, ResetPasswordSerializer, PayRateSerializer, BasicUserSerializer
from smartcare_appointments.schedule_logic import update_working_days

UserModel = get_user_model()


# Default auth is token auth, but this can't be used when *obtaining* the token originally
class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    """Tokens are revoked after different periods for different users:
    * superusers and admins have tokens revoked after the default Knox ttl
    * all other users have tokens revoked after 1 hour"""
    def get_token_ttl(self):
        context = self.get_context()
        request = context["request"]

        user_type = request.user.user_type
        if user_type in [0, 1]:
            return super().get_token_ttl()
        else:
            return timedelta(hours=1)


class UserFilter(filters.FilterSet):
    user_type = filters.MultipleChoiceFilter(choices=UserType.choices())

    class Meta:
        model = UserModel
        fields = ["user_type", "is_active"]


class UserView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    model = get_user_model()
    queryset = get_user_model().objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = UserFilter

    def get_permissions(self):
        # Anyone can register a user, only clinic staff can view other users data (users can access their own data via /api/user/me/)
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action in ["update", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        elif self.action in ["me", "staff", "update_password"]:
            return [permissions.IsAuthenticated()]
        elif self.action in ["make_active", "make_inactive", "make_full_time", "make_part_time", "set_pay_rate"]:
            return [IsAdmin()]
        else:
            return [IsStaff()]

    @action(detail=False)
    def me(self, request):
        user = UserSerializer(request.user, context={"request": request})
        return Response(user.data)

    @action(detail=False, methods=["POST"])
    def update_password(self, request):
        new_password = request.data.get("new_password")
        if new_password is None:
            return Response({"detail": "No new password provided"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()

        return Response({"detail": "Password updated"}, status=status.HTTP_200_OK)

    @staticmethod
    def verify_user_ids(user_ids):
        if not user_ids:
            return Response({"detail": "No users provided"}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(user_ids, list) or not all(isinstance(element, int) for element in user_ids):
            return Response({"detail": "The users field must be a list of ids"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def make_active(self, request):
        user_ids = request.data.get("users")

        response_or_none = self.verify_user_ids(user_ids)
        if response_or_none:
            return response_or_none

        updated_users = UserModel.objects.filter(pk__in=user_ids).update(is_active=True)
        return Response({"detail": ngettext(
            "%d user account was successfully activated.",
            "%d user accounts were successfully activated.",
            updated_users,
        ) % updated_users}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def make_inactive(self, request):
        user_ids = request.data.get("users")

        response_or_none = self.verify_user_ids(user_ids)
        if response_or_none:
            return response_or_none

        updated_users = UserModel.objects.filter(pk__in=user_ids).update(is_active=False)
        return Response({"detail": ngettext(
            "%d user account was successfully deactivated.",
            "%d user accounts were successfully deactivated.",
            updated_users,
        ) % updated_users}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def make_full_time(self, request):
        user_ids = request.data.get("users")

        response_or_none = self.verify_user_ids(user_ids)
        if response_or_none:
            return response_or_none

        selected_users = UserModel.objects.filter(
            pk__in=user_ids, user_type__in=[UserType.DOCTOR, UserType.NURSE],
            staff_info__isnull=False).all()

        for user in selected_users:
            user.staff_info.employment_type = EmploymentType.FULL_TIME.value
            user.staff_info.save()
            update_working_days(user.staff_info)
            print(user.staff_info.employment_type)

        updated_users = len(selected_users)
        if updated_users == 0:
            return Response({"detail": "No staff members selected"}, status=status.HTTP_403_FORBIDDEN)

        return Response({"detail": ngettext(
            "%d staff member was successfully made full time.",
            "%d staff members were successfully made full time.",
            updated_users,
        ) % updated_users}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def make_part_time(self, request):
        user_ids = request.data.get("users")

        response_or_none = self.verify_user_ids(user_ids)
        if response_or_none:
            return response_or_none

        selected_users = UserModel.objects.filter(
            pk__in=user_ids, user_type__in=[UserType.DOCTOR, UserType.NURSE],
            staff_info__isnull=False).all()

        for user in selected_users:
            user.staff_info.employment_type = EmploymentType.PART_TIME.value
            user.staff_info.save()
            update_working_days(user.staff_info)

        updated_users = len(selected_users)
        if updated_users == 0:
            return Response({"detail": "No staff members selected"}, status=status.HTTP_403_FORBIDDEN)

        return Response({"detail": ngettext(
            "%d staff member was successfully made part time.",
            "%d staff members were successfully made part time.",
            updated_users,
        ) % updated_users}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def set_pay_rate(self, request):
        user_ids = request.data.get("users")
        payrate_id = request.data.get("payrate")

        if payrate_id is None:
            return Response({"detail": "No payrate provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payrate = PayRate.objects.get(pk=payrate_id)
        except PayRate.DoesNotExist:
            return Response({"detail": "The payrate provided does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        response_or_none = self.verify_user_ids(user_ids)
        if response_or_none:
            return response_or_none

        selected_users = UserModel.objects.filter(
            pk__in=user_ids, user_type__in=[UserType.DOCTOR, UserType.NURSE],
            staff_info__isnull=False).all()

        for user in selected_users:
            user.staff_info.payrate = payrate
            user.staff_info.save()

        updated_users = len(selected_users)
        if updated_users == 0:
            return Response({"detail": "No staff members selected"}, status=status.HTTP_403_FORBIDDEN)

        return Response({"detail": ngettext(
            "%d staff member was successfully set to the payrate %s.",
            "%d staff members were successfully set to the payrate %s.",
            updated_users,
        ) % (updated_users, payrate)}, status=status.HTTP_200_OK)

    @staticmethod
    def set_patient_pay_type(request, pay_type):
        user_ids = request.data.get("users")

        response_or_none = UserView.verify_user_ids(user_ids)
        if response_or_none:
            return response_or_none

        selected_users = UserModel.objects.filter(
            pk__in=user_ids, user_type=UserType.PATIENT,
            patient_info__isnull=False).all()

        for user in selected_users:
            user.patient_info.pay_type = pay_type
            user.patient_info.save()

        updated_users = len(selected_users)
        if updated_users == 0:
            return Response({"detail": "No patients selected"}, status=status.HTTP_403_FORBIDDEN)

        return Response({"detail": ngettext(
            "%d patient was successfully made %s patient.",
            "%d patients were successfully made %s patient.",
            updated_users,
        ) % (updated_users, "an NHS" if pay_type == PatientPayType.NHS else "a Private")}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def make_nhs_patient(self, request):
        return self.set_patient_pay_type(request, PatientPayType.NHS)

    @action(detail=False, methods=["POST"])
    def make_private_patient(self, request):
        return self.set_patient_pay_type(request, PatientPayType.PRIVATE)

    @action(detail=False)
    def staff(self, request):
        staff_members = UserModel.objects.filter(user_type__in=[UserType.DOCTOR, UserType.NURSE], is_active=True).all()
        serializer = BasicUserSerializer(staff_members, many=True)
        return Response(serializer.data)


class StaffView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = StaffSerializer
    queryset = StaffInfo.objects.all().prefetch_related('timeOff')
    permission_classes = [IsStaff]


class PasswordResetView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["POST"])
    def after(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        if not token:
            return Response({"detail": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password:
            return Response({"detail": "New password not provided"}, status=status.HTTP_400_BAD_REQUEST)

        password_reset = PasswordReset.objects.filter(token=token).first()
        if not password_reset:
            return Response({"detail": "Invalid password reset token"}, status=status.HTTP_400_BAD_REQUEST)

        user = UserModel.objects.filter(email=password_reset.email).first()
        if not user:
            return Response({"detail": "Invalid password reset token"}, status=status.HTTP_400_BAD_REQUEST)

        if not tokens.default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid password reset token"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password reset"}, status=status.HTTP_200_OK)


class PayRateView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PayRateSerializer
    queryset = PayRate.objects.all()
    permission_classes = [IsStaff]