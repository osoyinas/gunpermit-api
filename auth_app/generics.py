from rest_framework import generics
from oauth2_provider.contrib.rest_framework.permissions import (
    IsAuthenticatedOrTokenHasScope,
)
from .permissions import IsAdminOrReadOnly

class ReadableListAPIView (generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ["read"]


class ReadableRetrieveAPIView (generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ["read"]

class ReadableCreateAPIView (generics.CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    required_scopes = ["write"]


class ReadableListCreateAPIView (generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    required_scopes = ["read"]

class ReadableRetrieveUpdateDestroyAPIView (generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    required_scopes = ["read"]