from django.core.management import BaseCommand
from accounts.models import ResetToken
from django.db import transaction

class Command(BaseCommand):

    help = "Verifica tokens de redefinição de senha expirados e os desativa."

    def handle(self, *args, **kwargs):
        query = ResetToken.objects.filter(active=True)

        for token in query:

            if token.is_token_expired():
                token.mark_token_as_expired()

