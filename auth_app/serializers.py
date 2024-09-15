from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255,
    )
    password = serializers.CharField(
        max_length=24, min_length=8, write_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                "Correo o contraseña incorrectos.")
        return user

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class RegisterSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "repeat_password",
        )
        extra_kwargs = {
            "first_name": {
                "required": True,
            },
            "last_name": {
                "required": True,
            },
            "email": {
                "required": True,
            },
            "password": {
                "write_only": True,
                "required": True,
            },
            "repeat_password": {
                "write_only": True,
                "required": True,
            },
        }

    def validate(self, data):
        if data["password"] != self.initial_data["repeat_password"]:
            raise serializers.ValidationError(
                {"repeat_password": "Las contraseñas no coinciden."}
            )
        return data

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
