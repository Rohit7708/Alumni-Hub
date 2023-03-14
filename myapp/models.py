from django.db import models
from xmlrpc.client import Boolean
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid
import random

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

class Category(models.Model):

    title=models.CharField(max_length=100)
    detail=models.TextField(null=True)
    class Meta:
        verbose_name_plural='Categories'

    def __str__(self) -> str:
        return self.title

class QuizQuestion(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    question=models.TextField(null=True)
    opt_1=models.CharField(max_length=200)
    opt_2=models.CharField(max_length=200)
    opt_3=models.CharField(max_length=200)
    opt_4=models.CharField(max_length=200)
    level=models.CharField(max_length=200)
    time_limit=models.IntegerField()
    right_opt=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Questions'
    def __str__(self) -> str:
        return self.question

class UserSubmittedAnswer(models.Model):
    question=models.ForeignKey(QuizQuestion,on_delete=models.CASCADE)
    user=models.CharField(max_length=100,null=True)
    right_answer=models.CharField(max_length=200)

    class Meta:
        verbose_name_plural='User Submitted Answers'

class UserCategoryAttempts(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    user=models.CharField(max_length=100,null=True)
    attemt_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='User Attempts Category '


class UserImage(models.Model):
    user_id=models.CharField(max_length=200,null=True)
    image = models.ImageField(upload_to='images/')
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url




