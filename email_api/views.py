import time

from django.http import JsonResponse
from django.shortcuts import render
from .tasks import send_email

# Create your views here.
def send_email_view(request):
    # TODO: check this request and make sure it works (problem with curl on the view not responding)
    send_email.delay(request.POST['email'], request.POST['subject'], request.POST['body'])
    return JsonResponse({"status": "Email sent"})
