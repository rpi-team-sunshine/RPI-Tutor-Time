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


class Request(models.Model):
    request_by = models.CharField(max_length=30)
    accepted_by = models.CharField(max_length=30, null=True)
    for_class = models.CharField(max_length=30)
    description = models.CharField(max_length=300, null=True)
    MON = 'M'
    TUES = 'T'
    WED = 'W'
    THURS = 'R'
    FRI = 'F'
    SAT = 'S'
    SUN = 'U'
    DAYS_CHOICES = (
        (MON, 'Mon'),
        (TUES, 'Tues'),
        (WED, 'Wed'),
        (THURS, 'Thurs'),
        (FRI, 'Fri'),
        (SAT, 'Sat'),
        (SUN, 'Sun')
    )
    days = models.CharField(max_length=2, choices=DAYS_CHOICES)
    time = models.TimeField()

