# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib import admin

class Town(models.Model):
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name

class House(models.Model):
    town = models.ForeignKey(Town)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        #return self.town.name
        return self.name

class Room(models.Model):
    house = models.ForeignKey(House)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        #return self.house.town.name
        return self.name

class Booking(models.Model):
    room 		= models.ForeignKey(Room)
    bookingname = models.CharField(max_length=64)

    def __unicode__(self):
        #return self.room.house.town.name
        return self.bookingname
    class Admin:
        sort_by = ('room__house__town', )
    
class BookingOpts(admin.ModelAdmin):
    list_filter = ('room__house__town', )
    raw_id_admin = ('room', )

admin.site.register(Town)
admin.site.register(House)
admin.site.register(Room)
admin.site.register(Booking, BookingOpts)