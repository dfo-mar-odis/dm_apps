from django.apps import AppConfig


class eDNAConfig(AppConfig):
    name = 'edna'

    def ready(self):
        import edna.signals
