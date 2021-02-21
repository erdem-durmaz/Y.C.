from django.apps import AppConfig


class NotifsConfig(AppConfig):
    name = 'notifs'

    def ready(self): #method just to import the signals
    	import notifs.signals
