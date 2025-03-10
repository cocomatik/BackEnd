from django.shortcuts import render
from django.http import JsonResponse
from Accounts.models import UserAccount,Verification
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

import random
from django.core.mail import send_mail

@api_view(['POST'])
def login(request):
    email=request.data.get('email')
    otp = request.data.get('otp')

    try:
        verification = Verification.objects.get(email=email)
        if not verification.is_valid():
            return Response({'error': 'OTP has expired'}, status=400)
        if verification.otp != otp:
            return Response({'error': 'Invalid OTP'}, status=400)
    except Verification.DoesNotExist:
        return Response({'error': 'No OTP sent for this user'}, status=400)

    
    try:
        user = UserAccount.objects.get(email=email)  # Try to fetch the user by email
    except UserAccount.DoesNotExist:
        # Create a new user without a password (just email)
        user = UserAccount.objects.create(email=email,name=verification.name)

    token, created = Token.objects.get_or_create(user=user)
    verification.delete()
    return Response({'token': token.key, 'email': email})


@api_view(['POST'])
def logout(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Successfully logged out'}, status=200)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid request or user not logged in'}, status=400)


@api_view(['POST'])
def send_otp_login(request):
    name=request.data.get('name')
    email=request.data.get('email')
    otp = str(random.randint(100000, 999999))

    verification, created = Verification.objects.get_or_create(email=email)
    verification.otp = otp
    verification.name = name
    verification.save()

    subject = "Your OTP for Login"
    from_email = 'login.cocomatikofficial@gmail.com'
    message = f'''Dear {name},
    Use this OTP {otp} to login / register to cocomatiks. This OTP is valid for 5 minutes only!
    Please do not reply to this email with your password. We will never ask for your password, and we strongly discourage you from sharing it with anyone.'''

    send_mail(subject, message, from_email, [email])

    return Response({'message': "Login OTP sent successfully."})



