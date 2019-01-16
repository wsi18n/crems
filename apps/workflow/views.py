from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from workflow.models import Workflow, State, Transition, CustomField
from workflow.serializers import WorkflowSerializers, StateSerializers, TransitionSerializers, CustomFieldSerializers


class WorkflowList(generics.ListAPIView):
    queryset = Workflow.objects.filter(deleted=False)
    serializer_class = WorkflowSerializers

    def get_queryset(self):
        queryset = super(WorkflowList, self).get_queryset()
        workflow_id = self.request.GET.get('workflow_id')
        if workflow_id:
            queryset = queryset.filter(id=workflow_id)
        return  queryset

    def post(self, request, *args, **kwargs):
        # system_name = request.data.get('name')
        pass


class StateList(generics.ListAPIView):
    queryset = State.objects.filter(deleted=False)
    serializer_class = StateSerializers

    def get_queryset(self):
        queryset = super(StateList, self).get_queryset()
        return  queryset

    def post(self, request, *args, **kwargs):
        # system_name = request.data.get('name')
        pass


class TransitionList(generics.ListAPIView):
    queryset = Transition.objects.filter(deleted=False)
    serializer_class = TransitionSerializers

    def get_queryset(self):
        queryset = super(TransitionList, self).get_queryset()
        return  queryset

    def post(self, request, *args, **kwargs):
        # system_name = request.data.get('name')
        pass


class CustomFieldList(generics.ListAPIView):
    queryset = CustomField.objects.filter(deleted=False)
    serializer_class = CustomFieldSerializers

    def get_queryset(self):
        queryset = super(CustomFieldList, self).get_queryset()
        workflow_id = self.request.GET.get('workflow_id')
        if workflow_id:
            queryset = queryset.filter(workflow_id=workflow_id)
        return  queryset

    def post(self, request, *args, **kwargs):
        # system_name = request.data.get('name')
        pass


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_workflow_init_state(request):
    workflow_id = request.GET.get('workflow_id')
    init_state_obj = State.objects.filter(workflow_id=workflow_id, deleted=False, state_type='2').first()
    transition_info_list = []
    transition_queryset = Transition.objects.filter(deleted=False, from_state_id=init_state_obj.id, workflow_id=workflow_id).all()
    for transition in transition_queryset:
        transition_info_list.append(dict(transition_id=transition.id, transition_name=transition.name))
    state_info = {
        'transition': transition_info_list
    }
    return JsonResponse({"state_info": state_info})
