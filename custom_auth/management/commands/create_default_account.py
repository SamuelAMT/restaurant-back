#from django.core.management.base import BaseCommand
#from custom_auth.models import Account
#import uuid
#
#class Command(BaseCommand):
#    help = 'Create a default account'
#
#    def handle(self, *args, **kwargs):
#        default_account_id = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
#        default_account, created = Account.objects.get_or_create(
#            account_id=default_account_id,
#            defaults={"email": "default@example.com", "password": "defaultpassword"}
#        )
#        if created:
#            self.stdout.write(self.style.SUCCESS('Successfully created default account'))
#        else:
#            self.stdout.write(self.style.WARNING('Default account already exists'))