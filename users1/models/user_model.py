#models/user_model.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from .base_model import BaseModel

class UserManager(BaseUserManager):#add
    def create_user(self, email, username,password=None,**kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**kwargs)#create user instance
        user.set_password(password)#sets user passwords and hashing security
        user.save(using=self._db)#save user instance in a specified db
        return user
    
class User(AbstractUser,BaseModel):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    objects = UserManager()


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users_permissions',
    )
    def __str__(self):
        return self.email