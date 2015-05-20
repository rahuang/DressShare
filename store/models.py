from django.db import models
from django.contrib.auth.models import User
from users.models import *
from time import time

def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)

class Dress(models.Model):
    name = models.TextField()
    owner = models.ForeignKey(Profile)
    thumbnail = models.FileField(upload_to=get_upload_file_name, blank=True)

    def __unicode__(self):
        return "name: " + self.name + " owner: " + self.owner.user.username
        