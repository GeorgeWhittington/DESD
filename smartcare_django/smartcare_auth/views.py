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


class CreateUserView(CreateModelMixin, viewsets.GenericViewSet):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


# TODO: for testing only, crud shouldn't be available for users, and we don't want to expose the full list!!!
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
