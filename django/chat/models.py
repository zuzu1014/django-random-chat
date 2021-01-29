from django.db import models
from django.conf import settings

class Room(models.Model):
    
    status_choice = (
        
        ("pending", "pending"),
        ("matched","matched"),
        ("closed",'closed')
    )
    
    
    status = models.CharField(verbose_name="status", choices=status_choice, max_length=50)
    
    creater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="creater", null=True, blank=True)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participant", null=True, blank=True)
    
 

    
    class Meta:
        db_table = "room_table"
        verbose_name = "room"
        verbose_name_plural = "rooms"
        

        