import datetime
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django_gunpermit.settings import SIMPLE_JWT

ACCESS_TOKEN_LIFETIME = SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']


class LoggedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

    def get_existing_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        expiration_time = datetime.datetime.now(
            datetime.timezone.utc) + ACCESS_TOKEN_LIFETIME
        expires_in_ms = int(expiration_time.timestamp() *
                            1000)  # Convert to milliseconds
        return {
            "id": instance.id,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "provider": instance.auth_provider,
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "expires_in": expires_in_ms,
        }


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
        if user.auth_provider != "email":
            raise serializers.ValidationError(
                f"Intentalo con {user.auth_provider}.")
        return user


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
                "allow_blank": False,

            },
            "last_name": {
                "required": True,
                "allow_blank": False,
            },
            "email": {
                "required": True,
                "max_length": 255,
                "allow_blank": False,
            },
            "password": {
                "write_only": True,
                "required": True,
                "min_length": 8,
                "max_length": 24,
                "allow_blank": False,
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
        generated_username = validated_data["email"].split("@")[0]
        validated_data["username"] = generated_username

        del validated_data["repeat_password"]

        user = get_user_model().objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "email"
        )
        read_only_fields = ("id", "email")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError(
                {"new_password": "La nueva contraseña no puede ser igual a la anterior."}
            )
        if not self.context["request"].user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "Contraseña incorrecta."})
        if self.context["request"].user.auth_provider != "email":
            raise serializers.ValidationError(
                {"provider": "El proveedor de autenticación debe ser 'email'."}
            )
        return super().validate(attrs)


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
