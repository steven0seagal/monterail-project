from django.db import models
from django.utils import timezone
# Create your models here.
import datetime
import pytz

class Event(models.Model):

   
    name = models.CharField(max_length=128, unique=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.name


class Ticket(models.Model):

    
    event = models.ForeignKey(Event,  on_delete=models.CASCADE)
    type = models.CharField(max_length=128)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    sold_status = models.BooleanField(default=False)
    reserved = models.BooleanField(default = False)
    payment_status = models.CharField(max_length=128, default='none')
    reserved_until = models.DateTimeField(default=datetime.datetime(2012, 1, 1, 12, 0, 0,tzinfo=pytz.UTC))
    reservation_number = models.CharField(max_length=28)