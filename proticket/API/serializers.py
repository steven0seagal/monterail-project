from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Event, Ticket
from django.contrib.auth.models import User


class EventSerializer(serializers.HyperlinkedModelSerializer):

    # name = serializers.CharField(max_length=128)
    # date = serializers.DateTimeField()
    class Meta:
        model = Event
        fields = ('id','name','date')

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
        
    #     return Event.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.name = validated_data.get('name', instance.title)
        
    #     instance.save()
    #     return instance
    


class TicketSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ticket
        # fields = ('event','type','price', 'sold_status', 'reserved', 'payment_status', 'reserved_until','reservation_number')
        fields = '__all__'
    # TICKET_TYPE_CHOICES = [
    #     ("REGULAR", 'regular'),
    #     ("BUDGET", 'budget'),
    #     ("PREMIUM", 'premium'),
    #     ("VIP", 'vip')]

    # PAYMENT_STATUS_CHOICES = [
    #     ("NONE", 'none'),
    #     ("STARTED", 'started'),
    #     ("PAYED", 'payed'),
    #     ("ERROR", 'error')]

    
    # event = EventSerializer()
    # type = serializers.CharField(max_length=256)
    # price = serializers.DecimalField(max_digits=10, decimal_places=2)
    # sold_status = serializers.BooleanField(default=False)
    # reserved = serializers.BooleanField(default=False)
    # payment_status = serializers.CharField(max_length=256, default='none')
    # reserved_untill = serializers.DateTimeField()

    

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
        
    #     return Ticket.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.id = validated_data.get('id', instance.title)
        
    #     instance.save()
    #     return instance


