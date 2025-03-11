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


from django.core.mail import EmailMultiAlternatives, send_mail
from resend import Emails
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import resend
from django.conf import settings

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

    otp = str(random.randint(100000, 999999))

    # Email Content
    html_content = render_to_string(
        'Accounts/login_email.html',
        {'name': name, 'otp': otp, 'status': status}
    )
    plain_text_content = strip_tags(html_content)

    # Try sending via Gmail SMTP
    try:
        with get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            email_message = EmailMultiAlternatives(
                subject=f"🔒 OTP for {status} - COCOMATIK Account",
                body=plain_text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
                connection=connection
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

        return Response({'message': f"OTP sent successfully for {status} using Gmail SMTP."})

    # If Gmail fails, try Brevo SMTP
    except Exception as gmail_error:
        try:
            with get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host=settings.BREVO_EMAIL_HOST,
                port=settings.BREVO_EMAIL_PORT,
                username=settings.BREVO_EMAIL_HOST_USER,
                password=settings.BREVO_EMAIL_HOST_PASSWORD,
                use_tls=settings.BREVO_EMAIL_USE_TLS
            ) as connection:
                email_message = EmailMultiAlternatives(
                    subject=f"🔒 OTP for {status} - COCOMATIK Account",
                    body=plain_text_content,
                    from_email=settings.BREVO_EMAIL_HOST_USER,
                    to=[email],
                    connection=connection
                )
                email_message.attach_alternative(html_content, "text/html")
                email_message.send()

            return Response({'message': f"OTP sent successfully for {status} using Brevo SMTP."})

        # If Brevo also fails, fallback to Resend
        except Exception as brevo_error:
            resend.api_key = settings.RESEND_API_KEY
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": email,
                "subject": f"🔒 OTP for {status} - COCOMATIK Account",
                "html": html_content
            })

            return Response({'message': f"OTP sent successfully for {status} using Resend."})
