from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user_type = validated_data["user_type"]

        user = UserModel.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=user_type == 4  # Only patients are automatically activated!
        )
        user.user_type = user_type
        user.save(update_fields=["user_type"])

        return user

    class Meta:
        model = UserModel
        fields = ["url", "username", "email", "password", "user_type"]