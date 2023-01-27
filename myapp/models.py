from django.db import models
from xmlrpc.client import Boolean
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Room(models.Model):
    name=models.CharField(max_length=200)

class Message(models.Model):
    body = models.TextField()
    date= models.DateTimeField(default=datetime.now,blank=True)
    msg_sender=models.CharField(max_length=200)
    msg_reciver=models.CharField(max_length=200)
    
    def __str__(self):
        return self.body