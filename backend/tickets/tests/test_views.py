from faker import Faker
from mock import patch, Mock
from django.utils import timezone
from mock.mock import MagicMock
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tickets.exceptions import InvalidOperation
from tickets.tests.factories import TicketFactory
from tickets.tests.utils import expected_data
from users.tests.factories import UserFactory


class TicketListTestCase(APITestCase):
    @patch("tickets.views.get_ticket_query")
    def test_list_unauthenticated(self, mock_get_ticket_query):
        fake = Faker()
        expected = [fake.name(), fake.name(), fake.name()]
        mock_get_ticket_query.return_value = expected
        resp = self.client.get(reverse('tickets-list'))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == expected
        assert mock_get_ticket_query.call_count == 1
        assert not mock_get_ticket_query.call_args[0][0].is_authenticated

    @patch("tickets.views.get_ticket_query")
    def test_list_authenticated(self, mock_get_ticket_query):
        fake = Faker()
        expected = [fake.name(), fake.name(), fake.name()]
        mock_get_ticket_query.return_value = expected
        user = UserFactory()
        self.client.login(username=user.email, password='password')
        resp = self.client.get(reverse('tickets-list'))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == expected
        mock_get_ticket_query.assert_called_once_with(user)


class TicketDetailTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manager = UserFactory(is_manager=True)
        cls.worker = UserFactory(is_manager=False)
        cls.assigned_ticket = TicketFactory(creator=cls.manager, assignee=cls.worker)
        cls.unassigned_ticket = TicketFactory(creator=cls.manager)

    def test_access_by_manager(self):
        self.client.login(username=self.manager.email, password='password')
        resp = self.client.get(reverse('tickets-detail', kwargs={'pk': self.assigned_ticket.id}))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == expected_data(self.assigned_ticket)
        resp = self.client.get(reverse('tickets-detail', kwargs={'pk': self.unassigned_ticket.id}))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == expected_data(self.unassigned_ticket)

    def test_access_by_assignee(self):
        self.client.login(username=self.worker.email, password='password')
        resp = self.client.get(reverse('tickets-detail', kwargs={'pk': self.assigned_ticket.id}))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == expected_data(self.assigned_ticket)
        resp = self.client.get(reverse('tickets-detail', kwargs={'pk': self.unassigned_ticket.id}))
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_access_by_unauthorized_user(self):
        resp = self.client.get(reverse('tickets-detail', kwargs={'pk': self.assigned_ticket.id}))
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        resp = self.client.get(reverse('tickets-detail', kwargs={'pk': self.unassigned_ticket.id}))
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class CreateTicketTestCase(APITestCase):
    def setUp(self):
        self.manager = UserFactory(is_manager=True)
        patcher = patch("tickets.views.CreateTicketSerializer")
        self.mock_serializer = patcher.start()
        self.mock_is_valid = MagicMock()
        self.mock_create = MagicMock()
        self.mock_serializer.return_value = MagicMock()
        self.mock_serializer.return_value.is_valid = self.mock_is_valid
        self.mock_serializer.return_value.create = self.mock_create
        self.addCleanup(patcher.stop)

    def test_create_ticket(self):
        self.mock_is_valid.return_value = True
        self.client.login(username=self.manager.email, password='password')
        resp = self.client.post(reverse('tickets-create'), data={'name': 'test ticket'})
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.mock_is_valid.call_count == 1
        assert self.mock_create.call_count == 1
        assert self.mock_serializer.call_args[1]['data']['name'] == 'test ticket'

    def test_validation_failed(self):
        self.mock_is_valid.return_value = False
        self.client.login(username=self.manager.email, password='password')
        resp = self.client.post(reverse('tickets-create'), data={'name': 'test ticket'})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert self.mock_is_valid.call_count == 1
        assert self.mock_create.call_count == 0
        assert self.mock_serializer.call_args[1]['data']['name'] == 'test ticket'

    def test_non_managers_cannot_create_ticket(self):
        worker = UserFactory(is_manager=False)
        self.client.login(username=worker.email, password='password')
        resp = self.client.post(reverse('tickets-create'), data={'name': 'test ticket'})
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        assert not self.mock_serializer.called
        assert not self.mock_is_valid.called
        assert not self.mock_create.called

    def test_unauthorized_users_cannot_create_ticket(self):
        resp = self.client.post(reverse('tickets-create'), data={'name': 'test ticket'})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert not self.mock_serializer.called
        assert not self.mock_is_valid.called
        assert not self.mock_create.called


@patch("tickets.views.update_ticket_name")
class UpdateTicketTestCase(APITestCase):
    def setUp(self):
        self.ticket = TicketFactory()
        self.manager = self.ticket.creator
        self.worker = self.ticket.assignee

    def test_update_ticket(self, mock_update_ticket_name):
        expected_name = 'new ticket name'
        self.client.login(username=self.manager.email, password='password')
        resp = self.client.post(reverse('tickets-update', kwargs={'pk': self.ticket.id}), data={'ticket_name': expected_name})
        assert resp.status_code == status.HTTP_200_OK
        mock_update_ticket_name.assert_called_once_with(self.ticket, expected_name)

    def test_unauthorized_access(self, mock_update_ticket_name):
        expected_name = 'new ticket name'

        # unauthenticated users cannot update a ticket
        resp = self.client.post(reverse('tickets-update', kwargs={'pk': self.ticket.id}), data={'ticket_name': expected_name})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert not mock_update_ticket_name.called

        # workers cannot update a ticket
        self.client.login(username=self.worker.email, password='password')
        resp = self.client.post(reverse('tickets-update', kwargs={'pk': self.ticket.id}), data={'ticket_name': expected_name})
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        assert not mock_update_ticket_name.called

    def test_validation_failed(self, mock_update_ticket_name):
        self.client.login(username=self.manager.email, password='password')
        # posting without specifying a new ticket_name should cause 400 bad request
        resp = self.client.post(reverse('tickets-update', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert not mock_update_ticket_name.called


@patch("tickets.views.update_ticket_assignee")
class AssignTicketTestCase(APITestCase):
    def setUp(self):
        self.ticket = TicketFactory(assignee=None)
        self.manager = self.ticket.creator
        self.worker = UserFactory(is_manager=False)

    def test_assign_ticket(self, mock_update_ticket_assignee):
        self.client.login(username=self.manager.email, password='password')
        resp = self.client.post(reverse('tickets-assign', kwargs={'pk': self.ticket.id}), data={'assignee_id': self.worker.id})
        assert resp.status_code == status.HTTP_200_OK
        mock_update_ticket_assignee.assert_called_once_with(self.ticket, self.worker)

    def test_unauthorized_access(self, mock_update_ticket_assignee):
        # unauthenticated users cannot assign tickets
        resp = self.client.post(reverse('tickets-assign', kwargs={'pk': self.ticket.id}), data={'assignee_id': self.worker.id})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert not mock_update_ticket_assignee.called

        # managers cannot assign ticket creator by other managers
        manager2 = UserFactory(is_manager=True)
        self.client.login(username=manager2.email, password='password')
        resp = self.client.post(reverse('tickets-assign', kwargs={'pk': self.ticket.id}), data={'assignee_id': self.worker.id})
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        assert not mock_update_ticket_assignee.called

    def test_invalid_assignee_id(self, mock_update_ticket_assignee):
        self.client.login(username=self.manager.email, password='password')
        resp = self.client.post(reverse('tickets-assign', kwargs={'pk': self.ticket.id}), data={'assignee_id': 99})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert not mock_update_ticket_assignee.called


@patch("tickets.views.start_ticket")
class StartTicketTestCase(APITestCase):
    def setUp(self):
        self.ticket = TicketFactory()
        self.manager = self.ticket.creator
        self.worker = self.ticket.assignee

    def test_start_ticket(self, mock_start_ticket):
        self.client.login(username=self.worker.email, password='password')
        resp = self.client.post(reverse('tickets-start', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_200_OK
        mock_start_ticket.assert_called_once_with(self.ticket)

    def test_unauthorized_access(self, mock_start_ticket):
        # unauthenticated user cannot start ticket
        resp = self.client.post(reverse('tickets-start', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert not mock_start_ticket.called

        # worker who is not the assignee cannot start a ticket
        worker2 = UserFactory(is_manager=False)
        self.client.login(username=worker2.email, password='password')
        resp = self.client.post(reverse('tickets-start', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        assert not mock_start_ticket.called

    def test_invalid_operation(self, mock_start_ticket):
        mock_start_ticket.side_effect = InvalidOperation("test exception")
        self.client.login(username=self.worker.email, password='password')
        resp = self.client.post(reverse('tickets-start', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        mock_start_ticket.assert_called_once_with(self.ticket)


@patch("tickets.views.complete_ticket")
class CompleteTicketTestCase(APITestCase):
    def setUp(self):
        self.ticket = TicketFactory(started=timezone.now())
        self.manager = self.ticket.creator
        self.worker = self.ticket.assignee

    def test_complete_ticket(self, mock_complete_ticket):
        self.client.login(username=self.worker.email, password='password')
        resp = self.client.post(reverse('tickets-complete', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_200_OK
        mock_complete_ticket.assert_called_once_with(self.ticket)

    def test_unauthorized_access(self, mock_complete_ticket):
        # unauthenticated user cannot complete ticket
        resp = self.client.post(reverse('tickets-complete', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert not mock_complete_ticket.called

        # worker who is not the assignee cannot complete a ticket
        worker2 = UserFactory(is_manager=False)
        self.client.login(username=worker2.email, password='password')
        resp = self.client.post(reverse('tickets-complete', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        assert not mock_complete_ticket.called

    def test_invalid_operation(self, mock_complete_ticket):
        mock_complete_ticket.side_effect = InvalidOperation("test exception")
        self.client.login(username=self.worker.email, password='password')
        resp = self.client.post(reverse('tickets-complete', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        mock_complete_ticket.assert_called_once_with(self.ticket)


@patch("tickets.views.verify_ticket")
class VerifyTicketTestCase(APITestCase):
    def setUp(self):
        self.ticket = TicketFactory(started=timezone.now(), completed=timezone.now())
        self.manager = self.ticket.creator
        self.worker = self.ticket.assignee

    def test_verify_ticket(self, mock_verify_ticket):
        self.client.login(username=self.manager.email, password='password')
        resp = self.client.post(reverse('tickets-verify', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_200_OK
        mock_verify_ticket.assert_called_once_with(self.ticket)

    def test_unauthorized_access(self, mock_verify_ticket):
        # unauthenticated user cannot verify ticket
        resp = self.client.post(reverse('tickets-verify', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert not mock_verify_ticket.called

        # worker cannot verify ticket
        self.client.login(username=self.worker.email, password='password')
        resp = self.client.post(reverse('tickets-verify', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        assert not mock_verify_ticket.called

    def test_invalid_operation(self, mock_verify_ticket):
        mock_verify_ticket.side_effect = InvalidOperation("test exception")
        self.client.login(username=self.manager.email, password='password')
        resp = self.client.post(reverse('tickets-verify', kwargs={'pk': self.ticket.id}))
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        mock_verify_ticket.assert_called_once_with(self.ticket)
