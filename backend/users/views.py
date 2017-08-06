from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import F, Value as V
from django.db.models.functions import Concat

from users.models import User


class WorkerList(APIView):
    def check_permissions(self, request):
        return request.user.is_authenticated and request.user.is_manager

    def get(self, request, *args, **kwargs):
        data = (
            User.objects
            .is_worker()
            .annotate(
                user_id=F('id'),
                full_name=Concat('first_name', V(' '), 'last_name'),
            ).values(
                'user_id',
                'full_name'
            )
        )
        return Response(data, status=status.HTTP_200_OK)
