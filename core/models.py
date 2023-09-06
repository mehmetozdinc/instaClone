from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True



class ProfileUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    working_at = models.CharField(max_length=150, default='#', blank=True, null=True)
    profileimg = models.ImageField(upload_to='profile_imgs',default='blank_profile.jpg')

    def __str__(self):
        return self.user.username

