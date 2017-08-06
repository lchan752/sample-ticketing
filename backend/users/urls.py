from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

urlpatterns = [
    url(r'^workers/$', views.WorkerList.as_view(), name='worker-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)