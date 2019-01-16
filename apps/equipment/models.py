# coding=utf-8
from django.db import models
from workflow.models import BaseModel
from users.models import Department


class Machine(BaseModel):
    """
    设备
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True)
    equip_version = models.CharField(max_length=50, null=True)
    equip_type = models.CharField(max_length=50, null=True)
    equip_sn = models.CharField(max_length=255)
    equip_use = models.CharField(max_length=255, null=True)
    u_count = models.CharField(max_length=50)
    department = models.ForeignKey(Department, related_name='machine_department', on_delete=models.CASCADE,
                                   null=True)
    """
    上架
    """
    def up_to_unit(self, query_set_or_id_list):

        if isinstance(query_set_or_id_list, list):
            from computer_room.models import CabinetUnit
            cabinet_unit_set = CabinetUnit.objects.filter(id__in=query_set_or_id_list)

        elif isinstance(query_set_or_id_list, models.query.QuerySet):
            cabinet_unit_set = query_set_or_id_list

        else:
            raise TypeError('params should be query_set or unit id list')

        units_not_empty = cabinet_unit_set.filter(machine_id__isnull=False).count()
        if units_not_empty:
            print(cabinet_unit_set)
            print('机位非空')
            return False

        self.cabinet_units.set(cabinet_unit_set)
        cabinet_unit_set.update(used_department_id=self.department.id)

        return True

    """
    下架
    """
    def down_from_unit(self):
        self.cabinet_units.update(used_department_id=None)
        self.cabinet_units.clear()
