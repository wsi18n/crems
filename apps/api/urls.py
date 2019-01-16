from django.urls import re_path, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    re_path(r'^auth/$', obtain_jwt_token, name='auth'),
    re_path(r'^workflow/', include('workflow.urls')),
    re_path(r'^ticket/', include('ticket.urls')),
    re_path(r'^users/', include('users.urls')),
    re_path(r'^computer-room/', include('computer_room.urls')),
    re_path(r'^equipment/', include('equipment.urls')),

]
