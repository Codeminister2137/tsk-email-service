import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()
