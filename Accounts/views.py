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


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags




@api_view(['POST'])
def send_otp_login(request):
    email = request.data.get('email')

    # Retrieve user object or None
    user = UserAccount.objects.filter(email=email).first()

    if user:  # Email exists → Proceed with Login
        name = user.name if user.name else email
        status = 'LOGIN'
    else:  # Email does not exist → Proceed with Registration
        name = email
        status = 'REGISTRATION'

    # otp = str(random.randint(100000, 999999))
    otp = 000000

    Verification.objects.update_or_create(email=email,otp=otp)

    # Email Content
    html_content = render_to_string(
        'Accounts/login_email.html',
        {'name': name, 'otp': otp, 'status': status}
    )
    plain_text_content = strip_tags(html_content)

    email_message = EmailMultiAlternatives(
        subject=f"🔒 OTP for {status} - COCOMATIK Account",
        body=plain_text_content,
        from_email='cocomatikofficial@gmail.com',
        to=[email]
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

    return Response({'message': f"OTP sent successfully for {status}."})
