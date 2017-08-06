from random import choice

from channels.tests import ChannelTestCase
from datetime import timedelta

from django.test.testcases import TestCase
from django.utils import timezone
from mock.mock import patch, MagicMock, call
import json

from tickets.constants import websocket_events
from tickets.exceptions import InvalidOperation
from tickets.helpers import send_websocket_message, create_ticket, update_ticket_name, update_ticket_assignee, start_ticket, complete_ticket, verify_ticket, get_ticket_query
from tickets.models import Ticket
from tickets.tests.factories import TicketFactory
from tickets.tests.utils import expected_data
from users.consumers import get_user_group
from users.tests.factories import UserFactory


class SendWebSocketMessageTestCase(ChannelTestCase):

    @patch('tickets.serializers.WebSocketTicketSerializer')
    def test_send_websocket_message(self, mock_ticket_serializer):
        expected_ticket_serialized = 'ticket_serialized'
        mock_ticket_serializer_instance = MagicMock()
        mock_ticket_serializer_instance.data = expected_ticket_serialized
        mock_ticket_serializer.return_value = mock_ticket_serializer_instance
        ticket = TicketFactory()
        user1 = UserFactory()
        user2 = UserFactory()
        user1_group = get_user_group(user1.id)
        user2_group = get_user_group(user2.id)
        user1_group.add("test-channel1")
        user2_group.add("test-channel2")
        event = choice(websocket_events.ALL_EVENTS)
        send_websocket_message([user1, user2], ticket, event)
        actual_message1 = dict(self.get_next_message("test-channel1", require=True))
        actual_message2 = dict(self.get_next_message("test-channel2", require=True))
        expected_message = json.dumps({
            'event': event,
            'ticket': expected_ticket_serialized
        })
        assert actual_message1['text'] == expected_message
        assert actual_message2['text'] == expected_message
        mock_ticket_serializer.assert_called_once_with(instance=ticket)


class TicketHelpersTestCase(TestCase):
    @patch("tickets.helpers.send_websocket_message")
    def test_create_ticket(self, mock_send_websocket_message):
        expected_ticket_name = "test ticket"
        expected_creator = UserFactory()
        expected_assignee = UserFactory()
        actual = create_ticket(expected_ticket_name, expected_creator, assignee=expected_assignee)
        assert Ticket.objects.filter(name=expected_ticket_name, creator=expected_creator, assignee=expected_assignee).exists()
        assert not Ticket.objects.exclude(name=expected_ticket_name, creator=expected_creator, assignee=expected_assignee).exists()
        mock_send_websocket_message.assert_called_once_with(
            [expected_creator, expected_assignee],
            actual,
            websocket_events.TICKET_CREATED
        )

    @patch("tickets.helpers.send_websocket_message")
    def test_update_ticket(self, mock_send_websocket_message):
        ticket = TicketFactory()
        expected_ticket_name = "new ticket name"
        update_ticket_name(ticket, expected_ticket_name)
        ticket.refresh_from_db()
        assert ticket.name == expected_ticket_name
        mock_send_websocket_message.assert_called_once_with(
            [ticket.creator, ticket.assignee],
            ticket,
            websocket_events.TICKET_UPDATED
        )

    @patch("tickets.helpers.send_websocket_message")
    def test_assign_ticket(self, mock_send_websocket_message):
        previous_assignee = choice([None, UserFactory()])
        ticket = TicketFactory(assignee=previous_assignee)
        expected_assignee = UserFactory(is_manager=False)
        update_ticket_assignee(ticket, expected_assignee)
        ticket.refresh_from_db()
        assert ticket.assignee == expected_assignee
        mock_send_websocket_message.assert_has_calls(
            [call(
                [ticket.creator, expected_assignee],
                ticket,
                websocket_events.TICKET_ASSIGNED
            )],
            any_order=True
        )
        if previous_assignee:
            mock_send_websocket_message.assert_has_calls(
                [call(
                    [previous_assignee],
                    ticket,
                    websocket_events.TICKET_REASSIGNED
                )],
                any_order=True
            )

    @patch("tickets.helpers.send_websocket_message")
    def test_exception_raised_if_assigning_to_wrong_user_type(self, mock_send_websocket_message):
        ticket = TicketFactory(assignee=None)
        manager = UserFactory(is_manager=True)
        self.assertRaises(InvalidOperation, update_ticket_assignee, ticket, manager)
        assert not mock_send_websocket_message.called

    @patch("tickets.helpers.send_websocket_message")
    def test_start_ticket(self, mock_send_websocket_message):
        t1 = timezone.now()
        ticket = TicketFactory()
        start_ticket(ticket, start_time=t1)
        ticket.refresh_from_db()
        assert ticket.started == t1
        mock_send_websocket_message.assert_called_once_with(
            [ticket.creator, ticket.assignee],
            ticket,
            websocket_events.TICKET_STARTED
        )

    @patch("tickets.helpers.send_websocket_message")
    def test_exception_raised_if_starting_ticket_that_has_not_been_assigned(self, mock_send_websocket_message):
        ticket = TicketFactory(assignee=None)
        self.assertRaises(InvalidOperation, start_ticket, ticket)
        assert not mock_send_websocket_message.called

    @patch("tickets.helpers.send_websocket_message")
    def test_complete_ticket(self, mock_send_websocket_message):
        t0 = timezone.now() - timedelta(days=1)
        t1 = timezone.now()
        ticket = TicketFactory(started=t0)
        complete_ticket(ticket, complete_time=t1)
        ticket.refresh_from_db()
        assert ticket.completed == t1
        mock_send_websocket_message.assert_called_once_with(
            [ticket.creator, ticket.assignee],
            ticket,
            websocket_events.TICKET_COMPLETED
        )

    @patch("tickets.helpers.send_websocket_message")
    def test_exception_raised_if_completing_ticket_that_has_not_started(self, mock_send_websocket_message):
        ticket = TicketFactory()
        self.assertRaises(InvalidOperation, complete_ticket, ticket)
        assert not mock_send_websocket_message.called

    @patch("tickets.helpers.send_websocket_message")
    def test_verify_ticket(self, mock_send_websocket_message):
        t0 = timezone.now() - timedelta(days=1)
        t1 = timezone.now()
        ticket = TicketFactory(started=t0, completed=t0)
        verify_ticket(ticket, verify_time=t1)
        ticket.refresh_from_db()
        assert ticket.verified == t1
        mock_send_websocket_message.assert_called_once_with(
            [ticket.creator, ticket.assignee],
            ticket,
            websocket_events.TICKET_VERIFIED
        )

    @patch("tickets.helpers.send_websocket_message")
    def test_exception_raised_if_verify_ticket_that_has_not_completed(self, mock_send_websocket_message):
        ticket = TicketFactory()
        self.assertRaises(InvalidOperation, verify_ticket, ticket)
        assert not mock_send_websocket_message.called


class GetTicketsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        t0 = timezone.now() - timedelta(days=2)
        t1 = timezone.now() - timedelta(days=1)
        t2 = timezone.now()
        cls.manager1 = UserFactory(is_manager=True)
        cls.manager2 = UserFactory(is_manager=True)
        cls.worker1 = UserFactory(is_manager=False)
        cls.worker2 = UserFactory(is_manager=False)
        cls.ticket1_unassigned = TicketFactory(creator=cls.manager1, assignee=None)
        cls.ticket1_assigned = TicketFactory(creator=cls.manager1, assignee=cls.worker1)
        cls.ticket1_started = TicketFactory(creator=cls.manager1, assignee=cls.worker1, started=t0)
        cls.ticket1_completed = TicketFactory(creator=cls.manager1, assignee=cls.worker1, started=t0, completed=t1)
        cls.ticket1_verified = TicketFactory(creator=cls.manager1, assignee=cls.worker1, started=t0, completed=t1, verified=t2)
        cls.ticket2_unassigned = TicketFactory(creator=cls.manager2, assignee=None)
        cls.ticket2_assigned = TicketFactory(creator=cls.manager2, assignee=cls.worker2)
        cls.ticket2_started = TicketFactory(creator=cls.manager2, assignee=cls.worker2, started=t0)
        cls.ticket2_completed = TicketFactory(creator=cls.manager2, assignee=cls.worker2, started=t0, completed=t1)
        cls.ticket2_verified = TicketFactory(creator=cls.manager2, assignee=cls.worker2, started=t0, completed=t1, verified=t2)

    def test_get_tickets_by_manager(self):
        manager1_tickets = get_ticket_query(self.manager1)
        assert expected_data(self.ticket1_unassigned) in manager1_tickets
        assert expected_data(self.ticket1_assigned) in manager1_tickets
        assert expected_data(self.ticket1_started) in manager1_tickets
        assert expected_data(self.ticket1_completed) in manager1_tickets
        assert expected_data(self.ticket1_verified) in manager1_tickets
        assert expected_data(self.ticket2_unassigned) not in manager1_tickets
        assert expected_data(self.ticket2_assigned) not in manager1_tickets
        assert expected_data(self.ticket2_started) not in manager1_tickets
        assert expected_data(self.ticket2_completed) not in manager1_tickets
        assert expected_data(self.ticket2_verified) not in manager1_tickets

    def test_get_tickets_by_assignee(self):
        worker1_tickets = get_ticket_query(self.worker1)
        assert expected_data(self.ticket1_unassigned) not in worker1_tickets
        assert expected_data(self.ticket1_assigned) in worker1_tickets
        assert expected_data(self.ticket1_started) in worker1_tickets
        assert expected_data(self.ticket1_completed) in worker1_tickets
        assert expected_data(self.ticket1_verified) in worker1_tickets
        assert expected_data(self.ticket2_unassigned) not in worker1_tickets
        assert expected_data(self.ticket2_assigned) not in worker1_tickets
        assert expected_data(self.ticket2_started) not in worker1_tickets
        assert expected_data(self.ticket2_completed) not in worker1_tickets
        assert expected_data(self.ticket2_verified) not in worker1_tickets

    def test_get_tickets_by_unauthenticated_user(self):
        user = UserFactory()
        tickets = get_ticket_query(user)
        assert not tickets.exists()
