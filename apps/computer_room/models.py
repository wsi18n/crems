# coding=utf-8
from django.db import models
from workflow.models import BaseModel
from users.models import Department
from equipment.models import Machine


class ComputerRoom(BaseModel):
    """
    机房
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True)
    address = models.TextField(max_length=500, null=True)


class Cabinet(BaseModel):
    """
    机柜
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True)
    total_unit_number = models.CharField(max_length=255, null=True)
    used_unit_number = models.CharField(max_length=255, default='0')
    available_unit_number = models.CharField(max_length=255, null=True)
    cabinet_row = models.CharField(max_length=50)
    cabinet_col = models.CharField(max_length=50)
    computer_room = models.ForeignKey(ComputerRoom, related_name='computer_room', on_delete=models.CASCADE)
    plan_department = models.ForeignKey(Department, related_name='plan_department', on_delete=models.CASCADE)
    used_department = models.ForeignKey(Department, related_name='used_department', on_delete=models.CASCADE)


class CabinetUnit(BaseModel):
    """
    机位， 机柜Unit
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True)
    cabinet = models.ForeignKey(Cabinet, related_name='cabinet', on_delete=models.CASCADE)
    plan_department = models.ForeignKey(Department, related_name='cabinet_unit_plan_department',
                                        on_delete=models.CASCADE, null=True)
    used_department = models.ForeignKey(Department, related_name='cabinet_unit_used_department',
                                        on_delete=models.CASCADE, null=True)

    state = models.BooleanField(default=True)
    machine = models.ForeignKey(Machine, related_name='cabinet_units', on_delete=models.CASCADE, null=True)

