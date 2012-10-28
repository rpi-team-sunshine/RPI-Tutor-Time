from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Tutee(models.Model):
    user = models.OneToOneField(User)

    # Place other fields here such as
    # phone_number = models.PhoneNumberField() 
    # home_address = models.TextField()

class Tutor(Tutee):
    pass


"""
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Tutee.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
"""
