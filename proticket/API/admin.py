from django.contrib import admin
from .models import Event,Ticket
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    fields=['name','date']
admin.site.register(Event,EventAdmin)

class TicketAdmin(admin.ModelAdmin):
    fields=['event', 'type','price','sold_status','reserved','payment_status','reserved_until']
admin.site.register(Ticket,TicketAdmin)


