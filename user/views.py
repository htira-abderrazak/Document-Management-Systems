from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import RegisterSerializer
import requests

import environ


env = environ.Env()
environ.Env.read_env()
# Create your views here.
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        recaptcha_token = request.data.get("token")
        email = request.data.get("email")
        key= env("recaptcha_secret_key")
        verification_url = f"https://www.google.com/recaptcha/api/siteverify?secret={key}&response={recaptcha_token}"
        response = requests.post(verification_url)
        data = response.json()
        if not data["success"]:
            return JsonResponse(
                {"message": "reCAPTCHA verification failed"}, status=400
            )
        else:
            

            return super().create(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
