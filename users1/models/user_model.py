from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models, transaction
from .base_model import BaseModel

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        with transaction.atomic():
            user = self.model(email=email, username=username, **kwargs)
            user.set_password(password)

            # Check if profile_logo is provided
            profile_logo = kwargs.get("profile_logo")
            if profile_logo:
                user.profile_logo = profile_logo

            user.save(using=self._db)

            # Assign groups if provided
            group_names = kwargs.get("groups", [])
            for group_name in group_names:
                try:
                    # Check if the group exists, if not create it
                    group, created = Group.objects.get_or_create(name=group_name)
                    user.groups.add(group)                   
                except Group.DoesNotExist:
                    raise ValueError(f"Group {group_name} does not exist")
                
            # Assigning user with permissions
            permissions = kwargs.get("permissions", [])
            for perm_codename in permissions:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    user.user_permissions.add(permission)
                except Permission.DoesNotExist:
                    raise ValueError(f"Permission {perm_codename} does not exist")    

        return user

    def create_superuser(self, email, username, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if not kwargs.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True")
        if not kwargs.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, username, password, **kwargs)

class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)  
    first_name = models.CharField(max_length=30, blank=True)  
    last_name = models.CharField(max_length=30, blank=True)   # Optional last name
    profile_logo = models.ImageField(upload_to="profile_logos/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    @property
    def logo_url(self):
        if self.profile_logo:
            return self.profile_logo.url
        return None

    def __str__(self):
        return self.email