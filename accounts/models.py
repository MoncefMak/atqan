from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models

from core.abstract_class import UserAuditModel


class UserManager(BaseUserManager):
    def create_user(self, email, password, is_active=False):
        if not email:
            raise ValueError("Enter an email.")
        if not password:
            raise ValueError("A password is required.")

        user = self.model(
            email=self.normalize_email(email),
            is_active=is_active
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            is_active=True
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, UserAuditModel, PermissionsMixin):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    # Permissions
    is_superuser = models.BooleanField(default=False)
    is_managed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        # Set username to email if not provided
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
