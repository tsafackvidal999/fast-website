from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    
#profile_image = models.ImageField(upload_to='profile_images', null = True, blank=True) # null = True, blank=True pour non obligatoire
    #document = models.FileField(upload_to='docuùent',  null = True, blank=True)
# Create your models here.
    pass
