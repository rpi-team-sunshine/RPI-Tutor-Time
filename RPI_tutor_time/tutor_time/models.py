from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
class Tutee(models.Model):
   user = models.OneToOneField(User) 

class Tutor(Tutee):
    pass



