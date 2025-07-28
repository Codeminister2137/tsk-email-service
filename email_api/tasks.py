from celery import shared_task
import time

@shared_task
def send_email(email, subject, body):
    print('Sending email')
    time.sleep(5)
    return "Email sent"