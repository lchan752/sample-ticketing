from django.utils import timezone
from django.db.models import F, Value as V, Case, When, CharField
from django.db.models.functions import Concat

from tickets.constants.status import VERIFIED, COMPLETED, STARTED, ASSIGNED, UNASSIGNED
from tickets.exceptions import InvalidOperation
from tickets.models import Ticket
from tickets.constants import websocket_events
from users.consumers import get_user_group

import json


def send_websocket_message(users, ticket, event):
    from tickets.serializers import WebSocketTicketSerializer
    ser = WebSocketTicketSerializer(instance=ticket)
    msg = {
        'event': event,
        'ticket': ser.data
    }
    for user in users:
        group = get_user_group(user.id)
        group.send({'text': json.dumps(msg)})


def create_ticket(ticket_name, creator, assignee=None):
    ticket = Ticket.objects.create(
        name=ticket_name,
        creator=creator,
        assignee=assignee
    )
    users = [creator, assignee] if assignee else [creator]
    send_websocket_message(users, ticket, websocket_events.TICKET_CREATED)
    return ticket


def update_ticket_name(ticket, new_ticket_name):
    ticket.name = new_ticket_name
    ticket.save()
    users = [ticket.creator, ticket.assignee] if ticket.assignee else [ticket.creator]
    send_websocket_message(users, ticket, websocket_events.TICKET_UPDATED)


def update_ticket_assignee(ticket, assignee):
    if assignee.is_manager:
        raise InvalidOperation("Cannot assign a ticket to a manager. Must assign it to a worker")
    previous_assignee = ticket.assignee
    ticket.assignee = assignee
    ticket.save()
    send_websocket_message([ticket.creator, assignee], ticket, websocket_events.TICKET_ASSIGNED)
    if previous_assignee:
        send_websocket_message([previous_assignee], ticket, websocket_events.TICKET_REASSIGNED)


def unassign_ticket(ticket):
    if ticket.started or ticket.completed or ticket.verified:
        raise InvalidOperation("Cannot unassign a ticket if it has already started")
    previous_assignee = ticket.assignee
    ticket.assignee = None
    ticket.save()
    send_websocket_message([ticket.creator, previous_assignee], ticket, websocket_events.TICKET_UNASSIGNED)


def start_ticket(ticket, start_time=None):
    if not ticket.assignee:
        raise InvalidOperation("Cannot start a ticket that has not been assigned")
    start_time = start_time if start_time else timezone.now()
    ticket.started = start_time
    ticket.save()
    send_websocket_message([ticket.creator, ticket.assignee], ticket, websocket_events.TICKET_STARTED)


def complete_ticket(ticket, complete_time=None):
    if not ticket.started:
        raise InvalidOperation("Cannot complete a ticket that has not started")
    complete_time = complete_time if complete_time else timezone.now()
    ticket.completed = complete_time
    ticket.save()
    send_websocket_message([ticket.creator, ticket.assignee], ticket, websocket_events.TICKET_COMPLETED)


def verify_ticket(ticket, verify_time=None):
    if not ticket.completed:
        raise InvalidOperation("Cannot verify a ticket that has not completed")
    verify_time = verify_time if verify_time else timezone.now()
    ticket.verified = verify_time
    ticket.save()
    send_websocket_message([ticket.creator, ticket.assignee], ticket, websocket_events.TICKET_VERIFIED)


def get_ticket_query(user):
    if not user.is_authenticated:
        return Ticket.objects.none()

    if user.is_manager:
        qry = Ticket.objects.created_by(user)
    else:
        qry = Ticket.objects.assigned_to(user)

    return (
        qry
        .annotate(
            ticket_id=F('id'),
            ticket_name=F('name'),
            creator_id=F('creator_id'),
            creator_fullname=Concat('creator__first_name', V(' '), 'creator__last_name'),
            creator_avatar=F('creator__avatar'),
            assignee_id=F('assignee_id'),
            assignee_fullname=Case(
                When(assignee__isnull=False, then=Concat('assignee__first_name', V(' '), 'assignee__last_name')),
                default=V(''),
                output_field=CharField(),
            ),
            assignee_avatar=F('assignee__avatar'),
            status=Case(
                When(verified__isnull=False, then=V(VERIFIED)),
                When(completed__isnull=False, then=V(COMPLETED)),
                When(started__isnull=False, then=V(STARTED)),
                When(assignee__isnull=False, then=V(ASSIGNED)),
                default=V(UNASSIGNED),
                output_field=CharField(),
            )
        )
        .values(
            'ticket_id',
            'ticket_name',
            'creator_id',
            'creator_fullname',
            'creator_avatar',
            'assignee_id',
            'assignee_fullname',
            'assignee_avatar',
            'status',
            'created',
            'started',
            'completed',
            'verified'
        )
    )
