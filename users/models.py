import uuid
from django.db import models
from django.contrib.auth.models import User,AbstractUser
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,blank=True,null=True)

    email = models.EmailField(blank=True,null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True,blank=True,upload_to='profiles/',default='profiles/user-default.png',help_text='You must upload original image before continuing.')
    location = models.CharField(max_length=500, blank=True, null=True)
    social_github = models.CharField(max_length=400, blank=True, null=True)
    social_twitter = models.CharField(max_length=400, blank=True, null=True)
    social_linkedln = models.CharField(max_length=400, blank=True, null=True)
    social_youtube = models.CharField(max_length=400, blank=True, null=True)
    social_website = models.CharField(max_length=400, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user)

class Skill(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True)
    recipient = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="messages")
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read']