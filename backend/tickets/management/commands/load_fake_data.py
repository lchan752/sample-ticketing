from random import choice

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from tickets.models import Ticket
from tickets.tests.factories import TicketFactory
from users.models import User
from users.tests.factories import UserFactory

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load fake data for development"

    def handle(self, *args, **options):
        """
        make 5 managers
        make 5 workers
        for each manager,
          make 1 unassigned ticket
          make 1 assigned ticket
          make 1 started ticket
          make 1 completed ticket
          make 1 verified ticket
          assign tickets to 1 of the 5 workers
        """
        logger.info("Deleting existing data ...")
        Ticket.objects.all().delete()
        User.objects.all().delete()

        logger.info("Loading fake development data ...")
        t0 = timezone.now() - timedelta(days=2)
        t1 = timezone.now() - timedelta(days=1)
        t2 = timezone.now()

        managers = UserFactory.create_batch(size=5, is_manager=True)
        UserFactory.reset_sequence()
        workers = UserFactory.create_batch(size=5, is_manager=False)
        for manager in managers:
            TicketFactory(creator=manager, assignee=None)
            TicketFactory(creator=manager, assignee=choice(workers))
            TicketFactory(creator=manager, assignee=choice(workers), started=t0)
            TicketFactory(creator=manager, assignee=choice(workers), started=t0, completed=t1)
            TicketFactory(creator=manager, assignee=choice(workers), started=t0, completed=t1, verified=t2)

        logger.info("Fake development data load complete.")
