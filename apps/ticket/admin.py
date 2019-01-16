from django.contrib import admin
from ticket.models import TicketRecord, TicketCustomField


class TicketRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'sn', 'title', 'workflow', 'current_state',
                    'is_end', 'is_rejected', 'creator')
    list_filter = ('created_at',)
    search_fields = ('title',)


class TicketCustomFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'field_key', 'char_value', 'ticket_record')
    list_filter = ('created_at',)
    search_fields = ('name',)

admin.site.register(TicketRecord, TicketRecordAdmin)
admin.site.register(TicketCustomField, TicketCustomFieldAdmin)