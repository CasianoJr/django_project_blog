from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    headshot = models.ImageField(
        default='user/default/headshot.svg', upload_to='user/profile', blank=True)

    def __str__(self):
        return f'{self.user.username}'

class Bio(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    bio = models.CharField(max_length=2000)

    def __str__(self):
        return f'{self.user.username}'


    # def get_absolute_url(self):
    #     return reverse("user-profile", kwargs={"pk": self.pk})