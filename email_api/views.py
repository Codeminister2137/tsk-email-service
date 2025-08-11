import time
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import render

from src.settings import project_settings


# from .tasks import send_email


# Create your views here.
@api_view(['POST'])
def send_email_view(request):
    data = request.data
    # send_email.delay(data['email'], data['subject'], data['body'])
    send_mail(subject=data['subject'],message=data['message'],from_email=project_settings.mail_adress,recipient_list=[data['recipient_list']])
    return Response({"message": "Email sent"}, status=status.HTTP_200_OK)
