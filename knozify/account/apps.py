from django.apps import AppConfig
from watson import search


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        user = self.get_model("User")
        search.register(user, fields=["username"])