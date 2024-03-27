from random import randint

from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user_type = validated_data["user_type"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        employment_type = validated_data.get("employment_type", None)

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

        
        if employment_type:
            user.employment_type = employment_type

            user.save(update_fields=["user_type","employment_type"])
        else: 
            user.save(update_fields=["user_type"])

        return user

    class Meta:
        model = UserModel
        fields = ["url", "username", "first_name", "last_name", "email", "password", "user_type","employment_type"]
        # Username is constructed from first+last name programatically, no validation needed
        extra_kwargs = {
            "username": {
                "validators": [],
                "read_only": True
            }
        }