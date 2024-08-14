from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager,
)
from django.db import models


class UserManager(DjangoUserManager):
    """Define a model manager for User model."""

    use_in_migrations = True

    def _create_user(self, username, password, telegram_id, **extra_fields):
        """Create and save a User with the given username, password, and telegram_id."""
        if not username:
            raise ValueError("The given username must be set")
        if not telegram_id:
            raise ValueError("The given telegram_id must be set")
        user = self.model(
            username=username,
            telegram_id=telegram_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, telegram_id=None, **extra_fields):
        """Create and save a regular User with the given username, password, and telegram_id."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, telegram_id, **extra_fields)

    def create_superuser(self, username=None, password=None, telegram_id=None, **extra_fields):
        """Create and save a SuperUser with the given username, password, and telegram_id."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(
            username,
            password,
            telegram_id,
            **extra_fields
        )


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    telegram_id = models.BigIntegerField(unique=True)

    first_name = None
    last_name = None

    REQUIRED_FIELDS = ["telegram_id"]
    objects = UserManager()

    def __str__(self):
        return self.username
