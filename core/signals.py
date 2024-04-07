import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Contact

@receiver(post_save, sender=Contact)
def generate_ticket_number(sender, instance, created, **kwargs):
    # Generate a unique 16-digit ticket number if the instance is newly created
    if created:
        ticket_number = ''.join(random.choices(string.digits, k=16))
        instance.contact_ticket = ticket_number
        instance.save()  # Save the instance after assigning the ticket number