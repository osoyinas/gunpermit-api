import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer
from auth_app.serializers import LoggedUserSerializer


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer
    permission_classes = []

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.get('auth_token')
        return Response(data, status=status.HTTP_200_OK)
