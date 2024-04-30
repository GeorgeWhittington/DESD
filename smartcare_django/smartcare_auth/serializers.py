from random import randint

from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth import get_user_model, tokens
from rest_framework import serializers

from smartcare_auth.models import StaffInfo, PayRate, UserType, PasswordReset, PatientInfo, PatientPayType
from smartcare_appointments.schedule_serializers import WorkingDaySerializer, TimeOffSerializer

UserModel = get_user_model()


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "first_name", "last_name"]


class StaffSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(required=True)
    working_days = WorkingDaySerializer(many=True, read_only=True)
    time_off = TimeOffSerializer(many=True, read_only=True,source='timeOff')
    class Meta:
        model = StaffInfo
        fields = ['user','employment_type','working_days', 'time_off']


#to display basic information within the user api
class StaffBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffInfo
        fields = ['user','employment_type']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    # not all users will need the staff serializer
    staff_info = StaffBasicSerializer(required=False)

    def create(self, validated_data):
        staff_info = validated_data.pop('staff_info', {})
        user_type = validated_data["user_type"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]

        fullname = f"{first_name}{last_name}"
        username = fullname

        # ensure un is unique
        while True:
            if UserModel.objects.filter(username=username).exists():
                rand_num = ''.join(["{}".format(randint(0, 9)) for num in range(0, 8)])
                username = f"{fullname}-{rand_num}"
            else:
                break

        user = UserModel.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=user_type == UserType.PATIENT,  # Only patients are automatically activated!
            is_staff=user_type <= UserType.ADMIN  # Admin and Superuser accounts can access the admin site
        )
        user.user_type = user_type
        user.save(update_fields=["user_type"])

        if user_type in [UserType.DOCTOR, UserType.NURSE]:
            if user_type == UserType.DOCTOR:
                payrate = PayRate.objects.get(Q(title="doctor"))
            else:
                payrate = PayRate.objects.get(Q(title="nurse"))

            StaffInfo(
                user=user,
                employment_type=staff_info.get('employment_type') if staff_info else None,
                payrate=payrate)

        if user_type == UserType.PATIENT:
            PatientInfo(user=user, pay_type=PatientPayType.PRIVATE)

        return user

    class Meta:
        model = UserModel
        fields = ["url", "id","username", "first_name", "last_name", "email", "password", "user_type", "staff_info"]
        # Username is constructed from first+last name programatically, no validation needed
        extra_kwargs = {
            "username": {
                "validators": [],
                "read_only": True
            }
        }


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        email = validated_data["email"]
        user = UserModel.objects.filter(email__iexact=email).first()

        # Don't tell attackers that an email does/does not exist in the system
        if not user:
            raise serializers.ValidationError("Password reset request failed")

        token = tokens.default_token_generator.make_token(user)

        password_reset = PasswordReset(email=email, token=token)
        password_reset.save()

        send_mail(
            "Your Smartcare Password Reset Request",
            f"""
Here's the password reset link you requested! If you didn't request a password reset, please ignore this email.

localhost:5173/reset-password/after/{token}
            """,
            "from@example.com",
            ["to@example.com", email],
            fail_silently=False,
        )

        return password_reset


    class Meta:
        model = PasswordReset
        fields = ["email"]