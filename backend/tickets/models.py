from django.db import models
from django.utils import timezone

from tickets.constants.status import VERIFIED, COMPLETED, STARTED, ASSIGNED, UNASSIGNED
from users.models import User
from tickets.querysets import TicketQuerySet


class Ticket(models.Model):
    name = models.TextField()
    creator = models.ForeignKey(User, related_name="tickets_created")
    assignee = models.ForeignKey(User, blank=True, null=True, related_name="tickets_assigned")
    created = models.DateTimeField(default=timezone.now)
    started = models.DateTimeField(blank=True, null=True)
    completed = models.DateTimeField(blank=True, null=True)
    verified = models.DateTimeField(blank=True, null=True)

    objects = TicketQuerySet.as_manager()

    def status(self):
        if self.verified:
            return VERIFIED
        elif self.completed:
            return COMPLETED
        elif self.started:
            return STARTED
        elif self.assignee:
            return ASSIGNED
        return UNASSIGNED
