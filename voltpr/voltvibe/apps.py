from django.apps import AppConfig

class VoltvibeConfig(AppConfig):
    name = 'voltvibe'

    def ready(self):
        import voltvibe.signals
