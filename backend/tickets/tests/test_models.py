from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from tickets.tests.factories import TicketFactory
from tickets.constants.status import VERIFIED, COMPLETED, STARTED, ASSIGNED, UNASSIGNED


class TicketTestCase(TestCase):
    def test_status(self):
        t0 = timezone.now() - timedelta(days=2)
        t1 = timezone.now() - timedelta(days=1)
        t2 = timezone.now()
        ticket_unassigned = TicketFactory(assignee=None)
        ticket_assigned = TicketFactory()
        ticket_started = TicketFactory(started=t0)
        ticket_completed = TicketFactory(completed=t1)
        ticket_verified = TicketFactory(verified=t2)
        assert ticket_unassigned.status() == UNASSIGNED
        assert ticket_assigned.status() == ASSIGNED
        assert ticket_started.status() == STARTED
        assert ticket_completed.status() == COMPLETED
        assert ticket_verified.status() == VERIFIED
