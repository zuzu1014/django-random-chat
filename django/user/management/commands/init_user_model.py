from django.core.management.base import BaseCommand, CommandError
from user.models import User

class Command(BaseCommand):
    help = 'Populates fake ussers.'

    def handle(self, *args, **options):
        User.objects.filter(is_staff=False).delete()
        
        
