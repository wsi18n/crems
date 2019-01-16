from django.urls import re_path
from users import views

urlpatterns = [
    re_path(r'^$', views.UserProfileList.as_view()),
    re_path(r'^department/$', views.DepartmentList.as_view()),
    re_path(r'^delete-user/$', views.delete_user),
    re_path(r'^update-user/$', views.update_user),
    re_path(r'^delete-department/$', views.delete_department),
    re_path(r'^update-department/$', views.update_department),
]
