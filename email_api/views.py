import time

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import render
from .tasks import send_email

# Create your views here.
@api_view(['POST'])
def send_email_view(request):
    # TODO: check this request and make sure it works (problem with curl on the view not responding)
    data = request.data
    send_email.delay(data['email'], data['subject'], data['body'])
    return Response({"message": "Email sent"}, status=status.HTTP_200_OK)
