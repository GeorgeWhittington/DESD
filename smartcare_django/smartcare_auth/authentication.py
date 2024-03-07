from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q


# from: https://stackoverflow.com/a/57153949
class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # Replicating django implementation so that timing attacks aren't possible
            # (attacker being able to discover whether a user exists or not based on how long different login requests take)
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
