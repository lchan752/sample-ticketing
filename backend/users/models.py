from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from users.querysets import UserQuerySet


class User(AbstractBaseUser):
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.URLField(blank=True)
    objects = UserQuerySet.as_manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name
