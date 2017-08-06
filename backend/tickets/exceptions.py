from rest_framework.views import exception_handler as default_exception_handler
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


class InvalidOperation(Exception):
    pass


def exception_handler(exc, context):
    response = default_exception_handler(exc, context)
    if response:
        return response

    if isinstance(exc, InvalidOperation):
        data = {'detail': str(exc)}
        return Response(data, status=HTTP_400_BAD_REQUEST)

    return None
