from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'board'

    def ready(self):
        import board.signals
        print("Signal registered!")
