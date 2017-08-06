import factory

from tickets.models import Ticket
from users.tests.factories import UserFactory


class TicketFactory(factory.DjangoModelFactory):
    name = """
    Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes,
    nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula. Cum sociis natoque penatibus et magnis dis parturient montes,
    nascetur ridiculus mus. Donec ullamcorper nulla non metus auctor fringilla. Duis mollis, est non commodo luctus, nisi erat
    porttitor ligula, eget lacinia odio sem nec elit. Donec ullamcorper nulla non metus auctor fringilla.
    """
    creator = factory.SubFactory(UserFactory, is_manager=True)
    assignee = factory.SubFactory(UserFactory, is_manager=False)

    class Meta:
        model = Ticket
