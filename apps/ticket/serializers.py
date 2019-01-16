from rest_framework import serializers
from ticket.models import TicketRecord
from computer_room import models as computer_room_m


class TicketRecordSerializers(serializers.ModelSerializer):
    workflow_name = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    current_state_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def get_workflow_name(self, obj):
        workflow = obj.workflow
        return workflow.name

    def get_creator_name(self, obj):
        creator = obj.creator
        return creator.username

    def get_current_state_name(self, obj):
        return '未通过' if obj.is_rejected else obj.current_state.name

    class Meta:
        model = TicketRecord
        fields = '__all__'
