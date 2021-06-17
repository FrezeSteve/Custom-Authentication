from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser
)
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from .managers import UserManager
import uuid


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    second_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    date_created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that is built in.

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active


class AnonymousUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(
        verbose_name='Session ID',
        max_length=255,
        unique=True
    )
    date_created = models.DateTimeField(default=timezone.now)
    last_used = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logged_in_user', null=True, blank=True)

    class Meta:
        verbose_name = 'AnonymousUser'
        verbose_name_plural = 'AnonymousUser'

    def __str__(self): return self.session_id
