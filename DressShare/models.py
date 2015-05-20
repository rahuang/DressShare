from django.db import models
from django.contrib.auth.models import User
from users.models import *


class Dress(models.Model):
    name = models.TextField()
    owner = models.ForeignKey(Profile)

    def __unicode__(self):
        return "name: " + self.name + " owner: " + self.owner
        
        
        