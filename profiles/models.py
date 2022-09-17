import uuid
import os 
from django.db import models
from accounts.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver 

def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('profiles/profile_images/',filename) 

def cover_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('profiles/cover_images/',filename) 

class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=200)
    # Custom Slug
    slug = models.CharField(max_length=250,unique=True,blank=True,null=True)
    email = models.EmailField(max_length=250)
    profile_image   = models.ImageField(upload_to=profile_image_path, blank=True, null=True)
    cover_image   = models.ImageField(upload_to=cover_image_path, blank=True, null=True)
    birthday = models.DateField(auto_now=False,auto_now_add=False,blank=True,null=True)
    gender = models.CharField(max_length=20,blank=True,null=True)
    
    # Date Only
    registered_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=False,auto_now_add=False,blank=True,null=True)

    def __str__(self):
        return self.full_name 

@receiver(post_delete,sender=Profile)
def profile_submission_delete(sender,instance,**kwargs):
    instance.profile_image.delete(False)
    instance.cover_image.delete(False)

def profile_pre_save_receiver(sender,instance, *args, **kwargs):
    if not instance.slug:
        title = instance.full_name.lower()
        words = title.split(' ')
        temp = ''
        for word in words:
            if word.strip() != '':
                word_separation = word.split('-')
                inner_temp = ''
                for x in word_separation:
                    if x.strip() != '':
                        if inner_temp != '':
                            inner_temp += f"-{x.strip()}"
                        else:
                            inner_temp += x.strip()
                if inner_temp != '':
                    if temp != '':
                        temp += f"-{inner_temp}"
                    else:
                        temp += inner_temp
        # Checking for existing slug
        profile_objs = Profile.objects.filter(slug=temp)
        if profile_objs.exists():
            temp += f"-{profile_objs.count()+1}"
        instance.slug = temp

pre_save.connect(profile_pre_save_receiver, sender=Profile)
