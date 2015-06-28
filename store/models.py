from django.db import models
from django.contrib.auth.models import User
from users.models import *
from time import time

def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)

class Dress(models.Model):
    name = models.TextField()
    owner = models.ForeignKey(User)
    picture = models.FileField(upload_to=get_upload_file_name, blank=True)
    description = models.TextField(blank=True)
    color = models.TextField()
    size = models.SmallIntegerField()

    LENGTH_CHOICES = (
        ('mini', 'Mini'),
        ('mid', 'Mid-Thigh'),
        ('knee', 'Knee'),
        ('tea', 'Tea'),
        ('long', 'Long'),
    )
    length = models.CharField(max_length=4, choices=LENGTH_CHOICES)

    FORMALITY_CHOICES = (
        ('B', 'Black-Tie'),
        ('C', 'Cocktail'),
        ('N', 'Night-Out'),
        ('D', 'Day-Time'),
    )
    formality = models.CharField(max_length=1, choices=FORMALITY_CHOICES)

    availability = models.BooleanField()

    def __unicode__(self):
        return "Dress(name: " + self.name + " owner: " + self.owner.username + ")"

class FittingRoom(models.Model):
    user = models.ForeignKey(User)
    dress = models.ForeignKey(Dress)

    def __unicode__(self):
        return "FittingRoom(name: " + str(self.user) + " dress: " + str(self.dress) + ")"

class Request(models.Model):
    user = models.ForeignKey(User)
    dress = models.ForeignKey(Dress)
    reason = models.TextField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    def __unicode__(self):
        return "Request(name: " + str(self.user) + " dress: " + str(self.dress) + ")"

class Borrowed(models.Model):
    user = models.ForeignKey(User)
    dress = models.ForeignKey(Dress)
    
    
    def __unicode__(self):
        return "Borrowed(name: " + str(self.user) + " dress: " + str(self.dress) + ")"