from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from tickets.models import Ticket
from tickets.helpers import update_ticket_name, update_ticket_assignee, start_ticket, complete_ticket, verify_ticket, get_ticket_query, unassign_ticket
from tickets.serializers import CreateTicketSerializer
from tickets.exceptions import exception_handler as tickets_exception_handler
from users.models import User


class AllowTicketCreatorOnly(object):
    def check_object_permissions(self, request, ticket):
        if ticket.creator != request.user:
            self.permission_denied(request, 'Only the ticket creator has permission to perform this action')


class AllowTicketAssigneeOnly(object):
    def check_object_permissions(self, request, ticket):
        if ticket.assignee != request.user:
            self.permission_denied(request, 'Only the ticket assignee has permission to perform this action')


class CreateTicket(APIView):
    def check_permissions(self, request):
        user = request.user
        if not user.is_authenticated or not user.is_manager:
            self.permission_denied(request, 'Only managers can create tickets')

    def post(self, request, *args, **kwargs):
        ser = CreateTicketSerializer(data=request.data, context={'request': request})
        if ser.is_valid():
            ser.create(ser.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            raise ValidationError(ser.errors)


class TicketBase(object):
    def get_queryset(self):
        return Ticket.objects.all()

    def get_exception_handler(self):
        return tickets_exception_handler


class UpdateTicketName(AllowTicketCreatorOnly, TicketBase, GenericAPIView):
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket_name = request.data.get('ticket_name', '')
        if not ticket_name:
            raise ValidationError({
                'ticket_name': 'This field is required'
            })
        update_ticket_name(ticket, ticket_name)
        return Response(status=status.HTTP_200_OK)


class AssignTicket(AllowTicketCreatorOnly, TicketBase, GenericAPIView):
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        assignee_id = request.data.get('assignee_id', None)
        try:
            assignee = User.objects.is_worker().get(id=assignee_id)
            update_ticket_assignee(ticket, assignee)
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise ValidationError({
                'assignee_id': 'Invalid assignee_id {}'.format(assignee_id)
            })


class UnassignTicket(AllowTicketCreatorOnly, TicketBase, GenericAPIView):
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        unassign_ticket(ticket)
        return Response(status=status.HTTP_200_OK)


class StartTicket(AllowTicketAssigneeOnly, TicketBase, GenericAPIView):
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        start_ticket(ticket)
        return Response(status=status.HTTP_200_OK)


class CompleteTicket(AllowTicketAssigneeOnly, TicketBase, GenericAPIView):
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        complete_ticket(ticket)
        return Response(status=status.HTTP_200_OK)


class VerifyTicket(AllowTicketCreatorOnly, TicketBase, GenericAPIView):
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        verify_ticket(ticket)
        return Response(status=status.HTTP_200_OK)


class TicketList(GenericAPIView):
    def get_queryset(self):
        return get_ticket_query(self.request.user)

    def get(self, request, *args, **kwargs):
        tickets = self.get_queryset()
        return Response(tickets, status=status.HTTP_200_OK)


class TicketDetail(GenericAPIView):
    def get_queryset(self):
        return get_ticket_query(self.request.user)

    def get(self, request, *args, **kwargs):
        ticket = self.get_object()
        return Response(ticket, status=status.HTTP_200_OK)
