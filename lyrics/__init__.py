# lyrics/__init__.py
default_app_config = 'lyrics.apps.LyricsConfig'

# lyrics/apps.py
from django.apps import AppConfig

class LyricsConfig(AppConfig):
    name = 'lyrics'

    def ready(self):
        import lyrics.signals