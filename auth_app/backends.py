from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('EEEEEEEEEEEEEEEEEE')
        print(username)

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None