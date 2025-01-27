from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,UserProfile

#creation of reciver function
@receiver(post_save, sender=User)
def post_save_create_profile_reciver(sender,instance,created, **kwargs):
  print(created)
  if created:
    UserProfile.objects.create(user=instance)
    #print("created user profile")
  else:
    try:
      profile=UserProfile.objects.get(user=instance) #if user profile is present then update it and save it using the instance
      profile.save
    except:
      #if user profile is not present(ie: user created from command line using createsuper cmd), then we need to create that userprofile
      UserProfile.objects.create(user=instance)
      #print("user was not present so created and updated")
    #print("user is updated")

@receiver(pre_save, sender=User)
def pre_save_create_profile_receiver(sender,instance,**kwargs):
  print(instance.username,"is created")