from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = '')
    description = models.TextField(default = '', blank = True)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):    
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()
