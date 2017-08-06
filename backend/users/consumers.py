from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from urllib.parse import parse_qs


def get_user_group(user_id):
    return Group("user-{}".format(user_id))


def get_user_from_jwt_token(message):
    qs = message.content.get('query_string')
    qs = qs.decode('utf8') if isinstance(qs, (bytes, bytearray)) else qs
    data = parse_qs(qs)
    token = data['token'][0] if 'token' in data else None
    ser = VerifyJSONWebTokenSerializer(data={'token': token})
    return ser.validated_data['user'] if ser.is_valid() else None


def accept_connection(message, user_id):
    message.reply_channel.send({"accept": True})
    group = get_user_group(user_id)
    group.add(message.reply_channel)


def reject_connection(message):
    message.reply_channel.send({"close": True})


@channel_session_user_from_http
def on_connect(message, user_id):
    user_id = int(user_id)
    if message.user.is_authenticated and message.user.id == user_id:
        accept_connection(message, user_id)
        return
    user = get_user_from_jwt_token(message)
    if user:
        accept_connection(message, user_id)
        return
    reject_connection(message)


@channel_session_user
def on_disconnect(message, user_id):
    group = get_user_group(user_id)
    group.discard(message.reply_channel)
