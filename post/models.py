from django.db import models
from tinymce.models import HTMLField
from django.shortcuts import reverse
from user.models import Profile
from django.db.models.signals import pre_save
from django.utils.text import slugify
import random
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    def get_slug(self):
        return self.name[:10]

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.TextField(max_length=1000)
    content = HTMLField('Content')
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_updated']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("post-update", kwargs={"slug": self.slug})
    
    def get_delete_url(self):
        return reverse("post-delete", kwargs={"slug": self.slug})

    def get_slug(self):
        return self.title[:10]

    # def delete(self, *args, **kwargs):
    #     if self.thumbnail:
    #         self.thumbnail.delete()
    #     super().delete(*args, **kwargs)

    @property
    def get_comments(self):
        return self.post_comment.all().order_by('-date_created')
    
    @property
    def get_images(self):
        return self.image_set.all()

class Image(models.Model):
    caption = models.CharField(max_length=150, blank=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)
    thumbnail = models.ImageField(
        blank=True, upload_to=f'post/%Y/%m/')

    def __str__(self):
        return f'{self.post.title[:15]} - Image'
    
    def get_slug(self):
        return self.caption[:10]

class Comment(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    post = models.ForeignKey(
        Post, related_name='post_comment', on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def get_slug(self):
        return self.comment[:10]

class ChildComment(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def get_slug(self):
        return self.comment[:10] 


@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Post)
@receiver(pre_save, sender=Comment)
@receiver(pre_save, sender=ChildComment)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.get_slug())       
        while sender.objects.filter(slug=instance.slug).exists():
            instance.slug += slugify(random.randint(0, 9))
        return instance.slug