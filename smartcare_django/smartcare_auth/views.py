from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.mixins import CreateModelMixin
from knox.views import LoginView as KnoxLoginView

from .serializers import UserSerializer


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
            return timedelta(hour=1)


class CreateUserView(CreateModelMixin, viewsets.GenericViewSet):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer