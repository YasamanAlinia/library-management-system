from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('A', 'Admin'),
        ('M', 'Member'),
        ('L', 'Librarian'),
    )

    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='M')

    def __str__(self):
        return self.username