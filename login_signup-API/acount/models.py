
# from distutils.command.upload import upload
# from email.mime import image
# from turtle import title
from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager,BaseUserManager
from datetime import *

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    
    email = models.EmailField(('Email Address'),unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    phone=models.CharField(max_length=20,null=True)
    age=models.IntegerField(null=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

class Product(models.Model):
    def nameFile(instance,filename):
        return '/'.join(['images',str(instance.title),filename])
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    price=MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    image=models.ImageField(upload_to=nameFile,blank=True)
    stock=models.BooleanField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

def __str__(self):
    return self.title
    