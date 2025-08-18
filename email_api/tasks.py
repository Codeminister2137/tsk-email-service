import logging

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from src.settings import project_settings

logger = logging.getLogger(__name__)


@shared_task
def send_email(html_template, context):
    from_email = project_settings.mail_adress  # Your email address
    subject = context.get("subject")
    to_email = context.get("to_email")
    cc = context.get("cc")
    bcc = context.get("bcc")
    attachments = context.get("attachments")

    if not to_email:
        raise ValueError("The 'to_email' address must be provided and cannot be empty.")
    elif not isinstance(to_email, list):
        to_email = [to_email]

    try:
        html_message = render_to_string(html_template, context)
        message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=from_email,
            to=to_email,
            cc=cc,
            bcc=bcc,
            attachments=attachments,
        )
        message.content_subtype = "html"
        result = message.send()
        logger.info(
            f"Sending email to {', '.join(to_email)} with subject: {subject} - Status {result}"
        )
    except Exception as e:
        logger.info(
            f"Sending email to {', '.join(to_email)} with subject: {subject} - Status 0"
        )
        logger.exception(e)
