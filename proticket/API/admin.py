from django.contrib import admin

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    fields=['id','date']