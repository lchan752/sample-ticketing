from django.db.models import QuerySet
from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string


class UserQuerySet(QuerySet):

    def create_user(self, email, first_name, last_name, password=None, is_manager=False, is_staff=False):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=BaseUserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_manager=is_manager,
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_worker(self, email, first_name, last_name, password):
        return self.create_user(email, first_name, last_name, password=password, is_manager=False, is_staff=False)

    def create_manager(self, email, first_name, last_name, password):
        return self.create_user(email, first_name, last_name, password=password, is_manager=True, is_staff=False)

    def create_superuser(self, email, first_name, last_name, password):
        return self.create_user(email, first_name, last_name, password=password, is_manager=False, is_staff=True)

    def get_by_natural_key(self, username):
        """
        From django.contrib.auth.models.BaseUserManager.get_by_natural_key
        """
        return self.get(**{self.model.USERNAME_FIELD: username})

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        From django.contrib.auth.models.BaseUserManager.make_random_password
        """
        return get_random_string(length, allowed_chars)

    def is_active(self):
        return self.filter(is_active=True)

    def not_active(self):
        return self.filter(is_active=False)

    def is_manager(self):
        return self.not_staff().filter(is_manager=True)

    def is_worker(self):
        return self.not_staff().filter(is_manager=False)

    def is_staff(self):
        return self.filter(is_staff=True)

    def not_staff(self):
        return self.filter(is_staff=False)