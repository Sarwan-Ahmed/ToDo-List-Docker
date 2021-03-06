"""Module to define view for socail auth"""
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .serializers import GoogleSocialAuthSerializer


class GoogleSocialAuthView(generics.GenericAPIView):
    """Social auth view for google"""
    serializer_class = GoogleSocialAuthSerializer
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
