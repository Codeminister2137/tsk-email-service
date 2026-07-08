import logging

from rest_framework.test import APIRequestFactory

from email_api.views import logger_test_view, send_email_view


def test_send_email_view_queues_email_with_default_template(monkeypatch):
    queued_calls = []

    class SendEmailTaskStub:
        def delay(self, *args):
            queued_calls.append(args)

    monkeypatch.setattr("email_api.views.send_email", SendEmailTaskStub())

    payload = {
        "subject": "Reminder",
        "to_email": ["recipient@example.com"],
        "message": "Task starts soon.",
    }
    request = APIRequestFactory().post("/email/", payload, format="json")

    response = send_email_view(request)

    assert response.status_code == 200
    assert response.data == {"message": "Email sent"}
    assert queued_calls == [("default_email_template.html", payload)]


def test_logger_test_view_logs_each_level(caplog):
    request = APIRequestFactory().get("/test/")

    with caplog.at_level(logging.DEBUG, logger="email_api.views"):
        response = logger_test_view(request)

    assert response.status_code == 200
    assert response.data == {"message": "Test message"}
    assert [record.levelname for record in caplog.records] == [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ]
    assert [record.message for record in caplog.records] == [
        "logger debug test",
        "logger info test",
        "logger warning test",
        "logger error test",
        "logger critical test",
    ]
