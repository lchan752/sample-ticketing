from channels.tests import ChannelTestCase, WSClient
from rest_framework_jwt.settings import api_settings
from urllib.parse import urlencode

from users.consumers import get_user_group
from users.tests.factories import UserFactory


class ConsumerFunctionalTestCase(ChannelTestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

    def test_unauthenticated_users_cannot_connect(self):
        client = WSClient()
        client.send_and_consume('websocket.connect', path='/users/{}/'.format(self.user1.id), check_accept=False)
        resp = client.receive()
        assert resp['close']
        group = get_user_group(self.user1.id)
        group.send({'text': 'ok'}, immediately=True)
        assert not client.receive()

    def test_user_cannot_connect_to_another_users_channel(self):
        client = WSClient()
        client.login(username=self.user2.email, password='password')
        client.send_and_consume('websocket.connect', path='/users/{}/'.format(self.user1.id), check_accept=False)
        resp = client.receive()
        assert resp['close']
        group = get_user_group(self.user1.id)
        group.send({'text': 'ok'}, immediately=True)
        assert not client.receive()

    def test_connect(self):
        client = WSClient()
        client.login(username=self.user1.email, password='password')
        client.send_and_consume('websocket.connect', path='/users/{}/'.format(self.user1.id))
        assert not client.receive()
        group = get_user_group(self.user1.id)
        group.send({'text': 'ok'}, immediately=True)
        assert client.receive(json=False) == 'ok'

    def test_jwt_connect(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user1)
        token = jwt_encode_handler(payload)

        client = WSClient()
        url = '/users/{}/'.format(self.user1.id) + '?' + urlencode({'token': token})
        client.send_and_consume('websocket.connect', path=url)
        assert not client.receive()
        group = get_user_group(self.user1.id)
        group.send({'text': 'ok'}, immediately=True)
        assert client.receive(json=False) == 'ok'

    def test_disconnect(self):
        client = WSClient()
        client.login(username=self.user1.email, password='password')
        client.send_and_consume('websocket.connect', path='/users/{}/'.format(self.user1.id))
        client.send_and_consume('websocket.disconnect', path='/users/{}/'.format(self.user1.id))
        group = get_user_group(self.user1.id)
        group.send({'text': 'ok'}, immediately=True)
        assert not client.receive()