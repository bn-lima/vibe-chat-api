from django.apps import AppConfig


class AccountProfileConfig(AppConfig):
    name = 'account_profile'

    def ready(self):
        import account_profile.signals