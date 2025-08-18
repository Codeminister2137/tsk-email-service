from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .tasks import send_email


# Create your views here.
@api_view(["POST"])
def send_email_view(request):
    data = request.data
    template = "default_email_template.html"
    send_email.delay(template, data)
    # send_mail(subject=data['subject'],message=data['message'],from_email=project_settings.mail_adress,recipient_list=[data['recipient_list']])
    return Response({"message": "Email sent"}, status=status.HTTP_200_OK)
