from random import randint

from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth import get_user_model, tokens
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from smartcare_auth.models import StaffInfo, PayRate, UserType, PasswordReset, PatientInfo, PatientPayType, EmploymentType
from smartcare_appointments.schedule_serializers import WorkingDaySerializer, TimeOffSerializer

UserModel = get_user_model()


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "first_name", "last_name", "email"]


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
        fields = ['employment_type', 'payrate']


class PatientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInfo
        fields = ["pay_type"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    # not all users will need the staff serializer
    staff_info = StaffBasicSerializer(required=False)
    patient_info = PatientInfoSerializer(required=False)

    patient_pay_type = serializers.IntegerField(write_only=True, required=False)

    def create(self, validated_data):
        user_type = validated_data["user_type"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]

        patient_pay_type = None
        if user_type == UserType.PATIENT:
            patient_pay_type = validated_data.get("patient_pay_type")
            print(patient_pay_type)
            if not (patient_pay_type in [PatientPayType.NHS, PatientPayType.PRIVATE]):
                raise ValidationError({"patient_pay_type_id": "Patient pay type is missing or unrecognised"})

        fullname = f"{first_name}{last_name}"
        username = fullname

        # ensure un is unique
        while True:
            if UserModel.objects.filter(username=username).exists():
                rand_num = ''.join(["{}".format(randint(0, 9)) for num in range(0, 8)])
                username = f"{fullname}-{rand_num}"
            else:
                break

        address_line_2 = validated_data["address_line_2"].strip()
        address_line_2 = address_line_2 if address_line_2 else None

        user = UserModel.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
            date_of_birth=validated_data["date_of_birth"],
            address_line_1=validated_data["address_line_1"],
            address_line_2=address_line_2,
            city=validated_data["city"],
            postcode=validated_data["postcode"],
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

            staff_info = StaffInfo(
                user=user,
                payrate=payrate)
            staff_info.save()

        if user_type == UserType.PATIENT:
            patient_info = PatientInfo(user=user, pay_type=patient_pay_type)
            patient_info.save()

        return user

    class Meta:
        model = UserModel
        fields = ["url", "id", "username", "first_name", "last_name", "email", "password", "user_type", "staff_info", "date_of_birth", "phone_number", "address_line_1", "address_line_2", "city", "postcode", "patient_info", "is_active", "patient_pay_type"]
        # Username is constructed from first+last name programatically, no validation needed
        # is_active should *not* ever be editable via this route
        extra_kwargs = {
            "username": {
                "validators": [],
                "read_only": True
            },
            "is_active": {
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


class PayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayRate
        fields = ["id", "title", "rate"]