from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username = username , email=email, **extra_fields)
        user.set_password(password) #this set_password do hashing means it hashes the password before storing
        user.save(using= self._db)  #this save the password in a database
        return user
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(username, email, password, **extra_fields)

#Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('vets', 'Veterinarian'),
        ('manager', 'Manager'),
    ]

    email = models.EmailField(unique=True)
    roles = models.CharField(max_length=255, choices=ROLE_CHOICES, default='manager')
    #Addition fields for user profile
    phone_number = models.CharField(max_length=10 , blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username




