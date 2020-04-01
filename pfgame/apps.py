from django.apps import AppConfig


class PfgameConfig(AppConfig):
    name = "pfgame"

    def ready(self):
        from . import signals
