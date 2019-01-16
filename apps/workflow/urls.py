from django.urls import re_path
from workflow import views

urlpatterns = [
    re_path(r'^$', views.WorkflowList.as_view()),
    re_path(r'^workflow-init-state/$', views.get_workflow_init_state),
    re_path(r'^state/$', views.StateList.as_view()),
    re_path(r'^transition/$', views.TransitionList.as_view()),
    re_path(r'^custom-field/$', views.CustomFieldList.as_view()),

]
