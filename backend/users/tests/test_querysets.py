from random import choice
from mock import patch

from django.test import TestCase
from faker import Faker

from users.models import User
from users.tests.factories import UserFactory


class UserQuerySetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.active_worker = UserFactory(is_manager=False, is_active=True)
        cls.inactive_worker = UserFactory(is_manager=False, is_active=False)
        cls.active_manager = UserFactory(is_manager=True, is_active=True)
        cls.inactive_manager = UserFactory(is_manager=True, is_active=False)
        cls.active_staff = UserFactory(is_staff=True, is_active=True)
        cls.inactive_staff = UserFactory(is_staff=True, is_active=False)

    def test_is_active(self):
        qry = User.objects.is_active()
        assert self.active_worker in qry
        assert self.inactive_worker not in qry
        assert self.active_manager in qry
        assert self.inactive_manager not in qry
        assert self.active_staff in qry
        assert self.inactive_staff not in qry

    def test_not_active(self):
        qry = User.objects.not_active()
        assert self.active_worker not in qry
        assert self.inactive_worker in qry
        assert self.active_manager not in qry
        assert self.inactive_manager in qry
        assert self.active_staff not in qry
        assert self.inactive_staff in qry

    def test_is_manager(self):
        qry = User.objects.is_manager()
        assert self.active_worker not in qry
        assert self.inactive_worker not in qry
        assert self.active_manager in qry
        assert self.inactive_manager in qry
        assert self.active_staff not in qry
        assert self.inactive_staff not in qry

    def test_is_worker(self):
        qry = User.objects.is_worker()
        assert self.active_worker in qry
        assert self.inactive_worker in qry
        assert self.active_manager not in qry
        assert self.inactive_manager not in qry
        assert self.active_staff not in qry
        assert self.inactive_staff not in qry

    def test_is_staff(self):
        qry = User.objects.is_staff()
        assert self.active_worker not in qry
        assert self.inactive_worker not in qry
        assert self.active_manager not in qry
        assert self.inactive_manager not in qry
        assert self.active_staff in qry
        assert self.inactive_staff in qry

    def test_not_staff(self):
        qry = User.objects.not_staff()
        assert self.active_worker in qry
        assert self.inactive_worker in qry
        assert self.active_manager in qry
        assert self.inactive_manager in qry
        assert self.active_staff not in qry
        assert self.inactive_staff not in qry


class CreateUserTestCase(TestCase):
    def test_create_user(self):
        fake = Faker()
        expected_first_name = fake.first_name()
        expected_last_name = fake.last_name()
        expected_email = fake.email()
        expected_staff = choice([True, False])
        expected_manager = choice([True, False])
        expected_password = 'cookiemonster'
        actual = User.objects.create_user(
            expected_email,
            expected_first_name,
            expected_last_name,
            password=expected_password,
            is_manager=expected_manager,
            is_staff=expected_staff
        )
        assert actual.email == expected_email
        assert actual.first_name == expected_first_name
        assert actual.last_name == expected_last_name
        assert actual.is_manager == expected_manager
        assert actual.is_staff == expected_staff
        assert actual.check_password(expected_password)

    def test_create_user_no_password(self):
        fake = Faker()
        expected_first_name = fake.first_name()
        expected_last_name = fake.last_name()
        expected_email = fake.email()
        expected_staff = choice([True, False])
        expected_manager = choice([True, False])
        actual = User.objects.create_user(
            expected_email,
            expected_first_name,
            expected_last_name,
            is_manager=expected_manager,
            is_staff=expected_staff
        )
        assert actual.email == expected_email
        assert actual.first_name == expected_first_name
        assert actual.last_name == expected_last_name
        assert actual.is_manager == expected_manager
        assert actual.is_staff == expected_staff
        assert not actual.has_usable_password()

    @patch('users.querysets.UserQuerySet.create_user')
    def test_create_worker(self, mock_create_user):
        fake = Faker()
        expected_first_name = fake.first_name()
        expected_last_name = fake.last_name()
        expected_email = fake.email()
        expected_password = 'cookiemonster'
        User.objects.create_worker(
            expected_email,
            expected_first_name,
            expected_last_name,
            expected_password
        )
        mock_create_user.assert_called_once_with(
            expected_email,
            expected_first_name,
            expected_last_name,
            password=expected_password,
            is_manager=False,
            is_staff=False
        )

    @patch('users.querysets.UserQuerySet.create_user')
    def test_create_manager(self, mock_create_user):
        fake = Faker()
        expected_first_name = fake.first_name()
        expected_last_name = fake.last_name()
        expected_email = fake.email()
        expected_password = 'cookiemonster'
        User.objects.create_manager(
            expected_email,
            expected_first_name,
            expected_last_name,
            expected_password
        )
        mock_create_user.assert_called_once_with(
            expected_email,
            expected_first_name,
            expected_last_name,
            password=expected_password,
            is_manager=True,
            is_staff=False
        )

    @patch('users.querysets.UserQuerySet.create_user')
    def test_create_staff(self, mock_create_user):
        fake = Faker()
        expected_first_name = fake.first_name()
        expected_last_name = fake.last_name()
        expected_email = fake.email()
        expected_password = 'cookiemonster'
        User.objects.create_superuser(
            expected_email,
            expected_first_name,
            expected_last_name,
            expected_password
        )
        mock_create_user.assert_called_once_with(
            expected_email,
            expected_first_name,
            expected_last_name,
            password=expected_password,
            is_manager=False,
            is_staff=True
        )
