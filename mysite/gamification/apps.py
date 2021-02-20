from django.apps import AppConfig


class GamificationConfig(AppConfig):
    name = 'gamification'

    def ready(self): #method just to import the signals
    	import gamification.signals
