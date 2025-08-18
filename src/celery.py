import os
from celery import Celery

# Remember poetry run celery -A src worker/flower -l info
#

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
app = Celery("src")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
