from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
    
    def ready(self) -> None:
        from .signals import create_metadata
        return super().ready()
    
    
