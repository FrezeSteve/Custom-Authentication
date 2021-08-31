from django.shortcuts import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.models import DeviceTracker
import uuid

User = get_user_model()


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self): return self.name


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200)
    body = models.TextField()
    published = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(null=True, blank=True)
    date_archived = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author", null=True)

    def __str__(self): return self.title

    class Meta:
        ordering = ('-date_created',)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})


class PostDeviceTracker(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='post_device_tracker')
    devices = models.ManyToManyField(DeviceTracker)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    published = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(null=True, blank=True)
    date_deleted = models.DateTimeField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    # who created or edited the comment.
    registered_user = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user", blank=True, null=True)
    device = models.ForeignKey(DeviceTracker, on_delete=models.CASCADE
                               , related_name="comment_anonymous_user")

    def __str__(self): return self.title

    class Meta:
        ordering = ('-date_created',)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.post.slug})
