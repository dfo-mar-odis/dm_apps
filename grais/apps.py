from django.apps import AppConfig


class GraisConfig(AppConfig):
    name = 'grais'

    def ready(self):
        import grais.signals
