from django.contrib.auth.models import AbstractUser, BaseUserManager
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
            if "profile_logo" in kwargs:
                user.profile_logo = kwargs["profile_logo"]

            user.save(using=self._db)

            # Assign groups if provided
            group_names = kwargs.get("groups", [])
            for group_name in group_names:
                group, _ = CustomGroups.objects.get_or_create(name=group_name)
                user.groups.add(group)

            # Assign permissions if provided
            permissions = kwargs.get("permissions", [])
            for perm_codename in permissions:
                permission = CustomPermissions.objects.filter(codename=perm_codename).first()
                if permission:
                    user.permissions.add(permission)
                else:
                    raise ValueError(f"Permission '{perm_codename}' does not exist")

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
    last_name = models.CharField(max_length=30, blank=True)  # Optional last name
    profile_logo = models.ImageField(upload_to="profile_logos/", null=True, blank=True)

    groups = models.ManyToManyField(
        "CustomGroups", blank=True, related_name="user_groups"
    )
    permissions = models.ManyToManyField(
        "CustomPermissions", blank=True, related_name="user_permissions"
    )

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


class CustomGroups(models.Model):
    name = models.CharField(max_length=150, unique=True)
    permissions = models.ManyToManyField(
        "CustomPermissions", blank=True, related_name="group_permissions"
    )

    def __str__(self):
        return self.name


class CustomPermissions(models.Model):
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=100)

    def __str__(self):
        return self.name
