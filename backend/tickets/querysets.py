from django.db.models import QuerySet


class TicketQuerySet(QuerySet):
    def created_by(self, creator):
        return self.filter(creator=creator)

    def assigned_to(self, assignee):
        return self.filter(assignee=assignee)

    def is_started(self):
        return self.filter(started__isnull=False)

    def is_completed(self):
        return self.filter(completed__isnull=False)

    def is_verified(self):
        return self.filter(verified__isnull=False)
