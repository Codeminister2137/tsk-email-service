# TSK Email Service

**Email microservice** for the TSK Task Scheduler (TSK) project (https://github.com/Codeminister2137/tsk).

This service is responsible for **sending email notifications** asynchronously. It exposes a REST endpoint that accepts email payloads and uses **Celery workers** to dispatch emails via Django’s mail system.

Documentation for this service can be provided via **MkDocs** in the `docs/` folder.

---

## Purpose

TSK Email Service is part of a microservices ecosystem that together implements a task scheduler. Alone it does nothing — it is designed to be run alongside:

* **Auth Service** — authentication and user identity
* **Calendar Service** — scheduling tasks and reminders
* **Main Orchestrator** — overall application composition

The calendar service or other clients send email requests to this service, which enqueues and sends them reliably.

---

## Tech Stack

* Python ≥ 3.10
* Django ≥ 5.1
* Django REST Framework
* Celery (task queue) with Redis support
* Flower (Celery monitoring UI)
* Poetry for dependency management
* HTML templates for email rendering

---

## Requirements

* Docker & Docker Compose (preferred for local development)
* Redis (for Celery queue)
* SMTP email account (configured via environment variables)
* Poetry (optional if running without Docker)

---

## Installation

Clone the repository:

```sh
git clone https://github.com/Codeminister2137/tsk-email-service.git
cd tsk-email-service
```

Install dependencies with Poetry:

```sh
poetry install
```

---

## Configuration

Configure environment variables such as:

* SMTP host, port
* Email credentials
* Redis broker URL
* Any other settings required by `src/settings.py`

---

## Running the Service

### With Docker Compose (Recommended)

If this service is part of the full TSK stack, start all services together:

```sh
docker compose up --build
```

This will start:

* Django application server
* Redis for Celery
* Celery workers
* Optional Flower UI

### Individually

Run Django development server:

```sh
poetry run python manage.py runserver
```

Start Celery worker (assuming Redis is configured):

```sh
poetry run celery -A src worker --loglevel=info
```

(Optional) Start Flower:

```sh
poetry run celery -A src flower
```

---

## API

### Send Email Endpoint

**POST** `/send/` (handled by `email_api/views.py`):

* Accepts JSON payload with email details
* Queues email for asynchronous sending via Celery

Example body:

```json
{
  "to_email": ["user@example.com"],
  "subject": "Reminder",
  "cc": [],
  "bcc": [],
  "attachments": []
}
```

The view delegates to the `send_email` Celery task, which constructs and sends the message.

---

## Email Sending Logic

Email sending is implemented as a Celery task in `email_api/tasks.py`. It:

1. Renders an HTML email using a template
2. Builds an `EmailMessage` object
3. Sends via the configured SMTP backend
4. Logs success or failure

This ensures that email dispatch is non-blocking and scalable.

---

## Repository Structure

```
email_api/             # Django app for email API
├── tasks.py           # Celery task for sending emails
├── views.py           # REST endpoint for email dispatch
├── apps.py            # Django app config
src/                   # Django project settings
manage.py
pyproject.toml         # Poetry project config
templates/             # HTML email templates
tests/                 # Unit / integration tests
docs/                  # MkDocs documentation source
```

---

## Monitoring

If using Flower, access its UI (default) at:

```
http://localhost:5555
```

to inspect Celery task queues and processing.

---

## Status

This service handles email dispatch and queuing. It does not implement business logic related to task scheduling — that is the responsibility of the calendar service. The service expects valid email data from other components.

---

## License

MIT License.
