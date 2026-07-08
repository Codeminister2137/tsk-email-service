import pytest

from email_api.tasks import send_email


def test_send_email_builds_and_sends_html_message(monkeypatch):
    rendered_messages = []
    sent_messages = []

    def render_template(template_name, context):
        rendered_messages.append((template_name, context))
        return "<p>Rendered body</p>"

    class EmailMessageStub:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.content_subtype = None

        def send(self):
            sent_messages.append(self)
            return 1

    monkeypatch.setattr("email_api.tasks.render_to_string", render_template)
    monkeypatch.setattr("email_api.tasks.EmailMessage", EmailMessageStub)
    monkeypatch.setattr("email_api.tasks.project_settings.mail_adress", "sender@example.com")

    context = {
        "subject": "Reminder",
        "to_email": "recipient@example.com",
        "cc": ["copy@example.com"],
        "bcc": ["hidden@example.com"],
        "attachments": [("report.txt", "content", "text/plain")],
    }

    send_email.run("default_email_template.html", context)

    assert rendered_messages == [("default_email_template.html", context)]
    assert len(sent_messages) == 1
    message = sent_messages[0]
    assert message.kwargs == {
        "subject": "Reminder",
        "body": "<p>Rendered body</p>",
        "from_email": "sender@example.com",
        "to": ["recipient@example.com"],
        "cc": ["copy@example.com"],
        "bcc": ["hidden@example.com"],
        "attachments": [("report.txt", "content", "text/plain")],
    }
    assert message.content_subtype == "html"


@pytest.mark.parametrize("to_email", [None, "", []])
def test_send_email_requires_recipient(to_email):
    with pytest.raises(ValueError, match="to_email"):
        send_email.run("default_email_template.html", {"to_email": to_email})


def test_send_email_keeps_list_recipient(monkeypatch):
    sent_messages = []

    class EmailMessageStub:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.content_subtype = None

        def send(self):
            sent_messages.append(self)
            return 1

    monkeypatch.setattr("email_api.tasks.render_to_string", lambda *_args: "<p>Body</p>")
    monkeypatch.setattr("email_api.tasks.EmailMessage", EmailMessageStub)

    send_email.run(
        "default_email_template.html",
        {"subject": "Status", "to_email": ["first@example.com", "second@example.com"]},
    )

    assert sent_messages[0].kwargs["to"] == ["first@example.com", "second@example.com"]


def test_send_email_logs_send_failure(monkeypatch, caplog):
    class EmailMessageStub:
        def __init__(self, **_kwargs):
            self.content_subtype = None

        def send(self):
            raise RuntimeError("SMTP unavailable")

    monkeypatch.setattr("email_api.tasks.render_to_string", lambda *_args: "<p>Body</p>")
    monkeypatch.setattr("email_api.tasks.EmailMessage", EmailMessageStub)

    with caplog.at_level("INFO", logger="email_api.tasks"):
        send_email.run(
            "default_email_template.html",
            {"subject": "Reminder", "to_email": "recipient@example.com"},
        )

    assert (
        "Sending email to recipient@example.com with subject: Reminder - Status 0"
        in caplog.messages
    )
    assert "SMTP unavailable" in caplog.text
