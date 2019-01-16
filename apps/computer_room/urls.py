from django.urls import re_path
from computer_room import views

urlpatterns = [
    re_path(r'^$', views.ComputerRoomList.as_view()),
    re_path(r'^cabinet/$', views.CabinetList.as_view()),
    re_path(r'^cabinet-unit/$', views.CabinetUnitList.as_view()),
    re_path(r'^delete-computer-room/$', views.delete_computer_room),
    re_path(r'^update-computer-room/$', views.update_computer_room),
    re_path(r'^delete-cabinet/$', views.delete_cabinet),
    re_path(r'^update-cabinet/$', views.update_cabinet),
    re_path(r'^delete-cabinet-unit/$', views.delete_cabinet_unit),
    re_path(r'^update-cabinet-unit/$', views.update_cabinet_unit),
]
