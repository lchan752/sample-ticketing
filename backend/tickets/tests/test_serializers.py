from django.test import TestCase
from django.test.client import RequestFactory
from mock.mock import patch
from rest_framework.reverse import reverse

from tickets.serializers import CreateTicketSerializer
from users.tests.factories import UserFactory


class CreateTicketSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.request = RequestFactory().get(reverse('tickets-create'))
        self.request.user = self.user

    def test_ticket_name_is_required(self):
        ser = CreateTicketSerializer(data={}, context={'request': self.request})
        assert not ser.is_valid()

    def test_assignee_is_optional(self):
        ser = CreateTicketSerializer(data={'name': 'new_ticket_name'}, context={'request': self.request})
        assert ser.is_valid()

    @patch("tickets.serializers.create_ticket")
    def test_create(self, mock_create):
        assignee = UserFactory(is_manager=False)
        ser = CreateTicketSerializer(
            data={'name': 'new_ticket_name', 'assignee': assignee.id},
            context={'request': self.request}
        )
        assert ser.is_valid()
        ser.create(ser.validated_data)
        mock_create.assert_called_once_with('new_ticket_name', self.user, assignee=assignee)
