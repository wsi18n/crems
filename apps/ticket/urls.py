from django.urls import re_path
from ticket import views

urlpatterns = [
    re_path(r'^$', views.TicketRecordList.as_view()),
    re_path(r'^ticket-flow-steps/$', views.get_ticket_flow_steps),
    re_path(r'^ticket-transitions/$', views.get_ticket_transitions),
    re_path(r'^ticket-custom-fields/$', views.get_ticket_custom_fields),
    re_path(r'^handle-ticket-state/$', views.handle_ticket_state),
]
