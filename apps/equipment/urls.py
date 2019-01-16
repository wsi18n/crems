from django.urls import re_path
from equipment import views

urlpatterns = [
    re_path(r'^$', views.MachineList.as_view()),
    re_path(r'^delete-machine/$', views.delete_machine),
    re_path(r'^update-machine/$', views.update_machine),

]
