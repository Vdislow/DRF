from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import User
from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

