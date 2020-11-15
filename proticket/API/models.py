from django.db import models

# Create your models here.


class Event(models.Model):

    id = models.AutoField(primary_key=True, editable=False)
    date = models.DateTimeField()



class Ticket(models.Model):

    TICKET_TYPE_CHOICES = [
        ("REGULAR", 'regular'),
        ("BUDGET", 'budget'),
        ("PREMIUM", 'premium'),
        ("VIP", 'vip')]

    PAYMENT_STATUS_CHOICES = [
        ("NONE", 'none'),
        ("STARTED", 'started'),
        ("PAYED", 'payed'),
        ("ERROR", 'error')]

       
    event = models.ForeignKey(Event,  on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=TICKET_TYPE_CHOICES)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    sold_status = models.BooleanField(default=False)
    reserved = models.BooleanField(default = False)
    payment_status = models.CharField(choices =PAYMENT_STATUS_CHOICES, max_length=16, default='none')
    reserved_until = models.DateTimeField()