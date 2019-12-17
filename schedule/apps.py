from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    name = 'schedule'

    def ready(self):
        from .utils import create_groups
