from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets, mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
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
            return timedelta(hours=1)


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_clinic_staff()


class UserView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    model = get_user_model()
    queryset = get_user_model().objects.all()

    def get_permissions(self):
        # Anyone can register a user, only clinic staff can view user data other than their own
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        elif self.action == "me":
            return [permissions.IsAuthenticated()]
        else:
            return [IsStaff()]

    @action(detail=False)
    def me(self, request):
        user = UserSerializer(request.user, context={"request": request})
        return Response(user.data)