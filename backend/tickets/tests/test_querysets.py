from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from tickets.models import Ticket
from tickets.tests.factories import TicketFactory
from users.tests.factories import UserFactory


class TicketQuerySetTestCase(TestCase):
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

    def test_created_by(self):
        qry = Ticket.objects.created_by(self.manager1)
        assert self.ticket1_unassigned in qry
        assert self.ticket1_assigned in qry
        assert self.ticket1_started in qry
        assert self.ticket1_completed in qry
        assert self.ticket1_verified in qry
        assert self.ticket2_unassigned not in qry
        assert self.ticket2_assigned not in qry
        assert self.ticket2_started not in qry
        assert self.ticket2_completed not in qry
        assert self.ticket2_verified not in qry

    def test_assigned_to(self):
        qry = Ticket.objects.assigned_to(self.worker1)
        assert self.ticket1_unassigned not in qry
        assert self.ticket1_assigned in qry
        assert self.ticket1_started in qry
        assert self.ticket1_completed in qry
        assert self.ticket1_verified in qry
        assert self.ticket2_unassigned not in qry
        assert self.ticket2_assigned not in qry
        assert self.ticket2_started not in qry
        assert self.ticket2_completed not in qry
        assert self.ticket2_verified not in qry

    def test_is_started(self):
        qry = Ticket.objects.is_started()
        assert self.ticket1_unassigned not in qry
        assert self.ticket1_assigned not in qry
        assert self.ticket1_started in qry
        assert self.ticket1_completed in qry
        assert self.ticket1_verified in qry
        assert self.ticket2_unassigned not in qry
        assert self.ticket2_assigned not in qry
        assert self.ticket2_started in qry
        assert self.ticket2_completed in qry
        assert self.ticket2_verified in qry

    def test_is_completed(self):
        qry = Ticket.objects.is_completed()
        assert self.ticket1_unassigned not in qry
        assert self.ticket1_assigned not in qry
        assert self.ticket1_started not in qry
        assert self.ticket1_completed in qry
        assert self.ticket1_verified in qry
        assert self.ticket2_unassigned not in qry
        assert self.ticket2_assigned not in qry
        assert self.ticket2_started not in qry
        assert self.ticket2_completed in qry
        assert self.ticket2_verified in qry

    def test_is_verified(self):
        qry = Ticket.objects.is_verified()
        assert self.ticket1_unassigned not in qry
        assert self.ticket1_assigned not in qry
        assert self.ticket1_started not in qry
        assert self.ticket1_completed not in qry
        assert self.ticket1_verified in qry
        assert self.ticket2_unassigned not in qry
        assert self.ticket2_assigned not in qry
        assert self.ticket2_started not in qry
        assert self.ticket2_completed not in qry
        assert self.ticket2_verified in qry
