from rest_framework import serializers

from tickets.helpers import create_ticket
from tickets.models import Ticket
from users.serializers import UserSerializer


class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['name', 'assignee']

    def create(self, validated_data):
        creator = self.context.get('request').user
        ticket = create_ticket(
            validated_data['name'],
            creator,
            assignee=validated_data.get('assignee', None)
        )
        return ticket


class WebSocketTicketSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    assignee = UserSerializer()
    creator = UserSerializer()

    class Meta:
        model = Ticket
        fields = ['id', 'name', 'assignee', 'creator', 'status', 'started', 'completed', 'verified']