import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from DMS import settings

from user.serializers import RegisterSerializer

import requests

import stripe

import environ

stripe.api_key = settings.STRIPE_SECRET_KEY

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
        
class Payment(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user

        if request.method == 'POST':
            data = json.loads(request.body)
            amount = data['amount']
            token = data['token']
            try:
                charge = stripe.Charge.create(
                    amount=int(amount * 100),  
                    currency='usd',
                    source=token,
                    description='Payment for order'
                )
                user.max_size= user.max_size+104857600
                user.save()
                return JsonResponse({'success': True})
            except stripe.error.StripeError as e:
                return JsonResponse({'success': False, 'error': str(e)})