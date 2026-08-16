from django.apps import AppConfig


class RestroomsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "restrooms"
    verbose_name = "Restrooms"

    def ready(self):
        from . import signals  # noqa: F401
