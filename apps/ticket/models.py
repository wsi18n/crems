from django.db import models
from django.utils.translation import ugettext_lazy as _
from workflow.models import Workflow, BaseModel, State
from users.models import UserProfile


class TicketRecord(BaseModel):
    """
    工单模型
    """
    sn = models.CharField(_('SN'), max_length=25)
    title = models.CharField(_('Title'), max_length=50, blank=True, default='')
    workflow = models.ForeignKey(Workflow, related_name='ticket_record_workflow', on_delete=models.CASCADE)
    current_state = models.ForeignKey(State, related_name='ticket_record_state', on_delete=models.CASCADE)
    participant_type = models.CharField(_('Participant Type'),
                                        choices=(
                                            ('1', 'person'),
                                            ('2', 'department')
                                        ),
                                        default='1',
                                        max_length=5)
    participant = models.ForeignKey(UserProfile, related_name='ticket_record_participant', on_delete=models.CASCADE, null=True, blank=True)
    related_user = models.ManyToManyField(UserProfile, related_name='ticket_record_related_user')
    is_end = models.BooleanField(default=False)
    is_rejected  = models.BooleanField(default=False)
    creator = models.ForeignKey(UserProfile, related_name='ticket_record_creator', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "工单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class TicketCustomField(BaseModel):
    """
    工单自定义字段， 工单自定义字段实际的值。
    """
    name = models.CharField(max_length=50, null=True, blank=True)
    char_value = models.CharField(max_length=255, null=True, blank=True)
    ticket_record = models.ForeignKey(TicketRecord, on_delete=models.CASCADE)
    field_key = models.CharField(max_length=50)

    class Meta:
        verbose_name = "自定义工单字段"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

