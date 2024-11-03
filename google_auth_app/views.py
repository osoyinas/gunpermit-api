from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import create_or_get_user, google_get_access_token, google_get_user_info
from auth_app.serializers import LoggedUserSerializer

class GoogleLoginCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')
        error = request.GET.get('error')

        if error or not code:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        domain = request.META['HTTP_HOST']
        redirect_uri = f'http://{domain}/api/google-login-callback/'

        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
        user_data = google_get_user_info(access_token=access_token)

        user = create_or_get_user(user_data)
        user_data = LoggedUserSerializer(user).data
        
        return Response(user_data, status=status.HTTP_200_OK)