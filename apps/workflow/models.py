# coding=utf-8
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from users.models import UserProfile


class Manager(models.Manager):
    def filter(self, *args, **kwargs):
        if not 'deleted' in kwargs.keys():  # 如果需要查看所有数据，
            kwargs['deleted'] = False
        return super().filter(*args, **kwargs)

    def exclude(self,*args, **kwargs):
        if not 'deleted' in kwargs.keys():
            kwargs['deleted'] = True
        return super().exclude(*args, **kwargs)

    def all(self):
        return self.filter()

    def count(self):
        return self.filter().count()

    def get(self, *args, **kwargs):
        return self.filter().get(*args, **kwargs)

class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = Manager()

    class Meta:
        abstract = True

    def fake_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()


class Workflow(BaseModel):
    """
    Instances of this class represent a named workflow that achieve a particular
    aim through a series of related states / transitions. A name for a directed
    graph.
    """

    name = models.CharField(_('Workflow Name'), max_length=50)
    description = models.CharField(_('Description'), max_length=50)
    flowchart = models.FileField(_('Flowchart'), upload_to='flowchart', blank=True, help_text='工作流的流程图')
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "工作流"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class State(BaseModel):
    """
    Represents a specific state that a thing can be in during its progress
    through a workflow. A node in a directed graph.
    """

    name = models.CharField(_('State Name'), max_length=50)
    description = models.CharField(_('Description'), max_length=50)
    workflow = models.ForeignKey(Workflow, related_name='state_workflow', on_delete=models.CASCADE)
    order_id = models.CharField(_('State Order'), max_length=10)
    state_type = models.CharField(_('State Type'),
                                  choices=(
                                      ('1', 'normal'),
                                      ('2', 'start'),
                                      ('3', 'end')
                                  ),
                                  default='1',
                                  max_length=5)
    participant_type = models.CharField(_('Participant Type'),
                                        choices=(
                                            ('1', 'person'),
                                            ('2', 'department')
                                        ),
                                        default='1',
                                        max_length=5)
    participant = models.ForeignKey(UserProfile, related_name='state_user', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "工作流状态"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Transition(BaseModel):
    """
    Represents how a workflow can move between different states. An edge
    between state "nodes" in a directed graph.
    """

    name = models.CharField(_('Transition Name'), max_length=50)
    description = models.CharField(_('Description'), max_length=50)
    transition_type = models.CharField(choices=(
        ('1', '同意'),
        ('2', '拒绝'),
        ('3', '其他')
    ), default='1', max_length=5)
    workflow = models.ForeignKey(Workflow, related_name='transitions', on_delete=models.CASCADE)
    from_state = models.ForeignKey(State, related_name='transitions_from', on_delete=models.CASCADE)
    to_state = models.ForeignKey(State, related_name='transitions_to', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "工作流流转"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CustomField(BaseModel):
    """
    Custom field in workflow
    """
    workflow = models.ForeignKey(Workflow, related_name='custom_field', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=50)
    description = models.CharField(_('Description'), max_length=50)
    field_key = models.CharField(max_length=50)
    field_type = models.CharField(
        max_length=5, choices=(
        ('5', '字符串'),
        ('10', '单选框'),
        ('15', '多选框'),
        ('20', '日期'),
        ('25', '日期时间'),
        ('30', '文本域'),
    ),
        default='5')

    class Meta:
        verbose_name = "工作流自定义字段"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.field_name
