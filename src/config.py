from django.core.management.utils import get_random_secret_key
from pydantic import Field

from pydantic_settings import BaseSettings


class ProjectSettings(BaseSettings):
    secret_key: str = Field(default_factory=get_random_secret_key)
    mail_adress: str
    mail_password: str

    model_config = {"env_file": "src/.env"}
