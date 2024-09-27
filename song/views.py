from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from .serializers import SignUpSerializer
from .serializers import ChangePasswordSerializer
from .serializers import UpdateProfileSerializer
from .serializers import AdminChangePasswordSerializer
from .serializers import AdminUpdateProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from .openapi import change_password_responses
from .openapi import CustomAutoSchema

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        AllowAny,
    )
    serializer_class = SignUpSerializer


class ChangePasswordView(generics.GenericAPIView):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
    # permission_classes = (
    #     IsAuthenticated,
    # )
    serializer_class = ChangePasswordSerializer
    swagger_schema = CustomAutoSchema

    @swagger_auto_schema(
        responses=change_password_responses,
        exmaple_paramters={
            'old_password': 'ABCD12345678',
            'password': 'ABCD123456789',
            'password2': 'ABCD123456789',
        },
    )
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({'success': True})


class UpdateProfileView(generics.GenericAPIView):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = UpdateProfileSerializer
    throttle_classes = [
        AnonRateThrottle,
        UserRateThrottle,
    ]

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({'success': True})


class AdminChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        IsAdminUser,
    )
    serializer_class = AdminChangePasswordSerializer

class AdminUpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        IsAdminUser,
    )
    serializer_class = AdminUpdateProfileSerializer
