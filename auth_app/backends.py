from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(username)
            user = get_user_model().objects.get(email=username)
            print(user)
        except get_user_model().DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
