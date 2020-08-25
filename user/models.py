from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=50, blank=True)
    headshot = models.ImageField(
        default='user/default/headshot.svg', upload_to='user/profile', blank=True)

    def __str__(self):
        return f'{self.user.username}'
    
    def get_absolute_url(self):
        return reverse('users', kwargs={'username': self.user.username})

class Bio(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    field = models.CharField(max_length=50, blank=True)
    field_description = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return f'{self.user.user.username} - {self.field}'


    # def get_absolute_url(self):
    #     return reverse("user-profile", kwargs={"pk": self.pk})