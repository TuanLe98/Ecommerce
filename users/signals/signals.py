from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete

from users.models import Profile
from django.dispatch import receiver

@receiver(post_save,sender = User)
def createProfile(sender,instance,created,**kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(user = user,
                                         name = user.username,
                                         email = user.email)

@receiver(post_save,sender = Profile)
def updateProfile(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.username = profile.name
        user.email = profile.email
        user.save()

@receiver(post_delete,sender = Profile)
def deleteUser(sender,instance,**kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
