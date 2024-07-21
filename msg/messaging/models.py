from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission



class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True,default='profile_photos/default-user-image.png')
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=True, null=True)  # Text content, optional if media is present
    media_file = models.FileField(upload_to='media_files/', blank=True, null=True)  # For files, videos
    media_image = models.ImageField(upload_to='media_images/', blank=True, null=True)  # For images
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'

        class Meta:
            ordering = ['-timestamp']