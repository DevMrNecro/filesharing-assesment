from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ops', 'Operations User'),
        ('client', 'Client User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class File(models.Model):
    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} uploaded by {self.uploader.username}"
