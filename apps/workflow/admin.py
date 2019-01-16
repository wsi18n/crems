from django.contrib import admin
from workflow.models import Workflow, State, Transition, CustomField


class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)


class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'workflow', 'order_id', 'state_type', 'participant_type', 'participant', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)


class TransitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'workflow', 'from_state', 'to_state', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)


class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'field_name', 'workflow', 'description', 'field_key')
    list_filter = ('created_at',)
    search_fields = ('field_name',)


admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(CustomField, CustomFieldAdmin)

