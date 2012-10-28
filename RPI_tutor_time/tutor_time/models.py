from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tutee(models.Model):
    user = models.OneToOneField(User)

    # Place other fields here such as
    # phone_number = models.PhoneNumberField() 
    # home_address = models.TextField()

class Tutor(Tutee):
    pass
