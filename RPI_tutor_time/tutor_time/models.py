from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Tutee(models.Model):
    user = models.OneToOneField(User)

    def is_tutor(self):
        try:
            self.tutor
        except Tutor.DoesNotExist:
            return False
        return True

    # Place other fields here such as
    # phone_number = models.PhoneNumberField() 
    # home_address = models.TextField()

class Tutor(Tutee):
    pass
