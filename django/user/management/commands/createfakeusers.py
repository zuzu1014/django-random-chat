from django.core.management.base import BaseCommand, CommandError
from user.models import User

class Command(BaseCommand):
    help = 'Populates fake ussers.'

    def handle(self, *args, **options):
        print("Populating...")
        for i in range(300):
            User.objects.create_user(user_id="dkanrjsk"+str(i), password="dkanrjsk"+str(i), email="dkanrjsk"+str(i)+"@gmail.com")
        print("Done.")
        
        
