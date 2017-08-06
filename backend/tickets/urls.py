from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from tickets import views

urlpatterns = [
    url(r'^$', views.TicketList.as_view(), name='tickets-list'),
    url(r'^create/$', views.CreateTicket.as_view(), name='tickets-create'),
    url(r'^(?P<pk>[0-9]+)/$', views.TicketDetail.as_view(), name='tickets-detail'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.UpdateTicketName.as_view(), name='tickets-update'),
    url(r'^(?P<pk>[0-9]+)/assign/$', views.AssignTicket.as_view(), name='tickets-assign'),
    url(r'^(?P<pk>[0-9]+)/unassign/$', views.UnassignTicket.as_view(), name='tickets-unassign'),
    url(r'^(?P<pk>[0-9]+)/start/$', views.StartTicket.as_view(), name='tickets-start'),
    url(r'^(?P<pk>[0-9]+)/complete/$', views.CompleteTicket.as_view(), name='tickets-complete'),
    url(r'^(?P<pk>[0-9]+)/verify/$', views.VerifyTicket.as_view(), name='tickets-verify'),
]

urlpatterns = format_suffix_patterns(urlpatterns)