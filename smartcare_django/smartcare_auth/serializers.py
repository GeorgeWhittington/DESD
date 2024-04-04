from random import randint
from smartcare_appointments.schedule_serializers import WorkingDaySerializer, TimeOffSerializer
from django.contrib.auth import get_user_model
from .models import Staff
from rest_framework import serializers

UserModel = get_user_model()



class StaffSerializer(serializers.ModelSerializer):
    working_days = WorkingDaySerializer(many=True, read_only=True)
    time_off = TimeOffSerializer(many=True, read_only=True,source='timeOff')
    class Meta:
        model = Staff
        fields = ['user','employment_type','working_days', 'time_off']

class StaffBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
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
            is_active=user_type == 5,  # Only patients are automatically activated!
            is_staff=user_type <= 1  # Admin and Superuser accounts can access the admin site
        )
        user.user_type = user_type

        user.save(update_fields=["user_type"])

        if user_type in [2, 3]:
            Staff.objects.create(user=user, employment_type=staff_info.get('employment_type') if staff_info else None)

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

