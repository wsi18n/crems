# coding=utf-8
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from equipment.models import Machine
from computer_room.models import CabinetUnit
from equipment.serializers import MachineSerializers


class MachineList(generics.ListAPIView):
    queryset = Machine.objects.filter(deleted=False)
    serializer_class = MachineSerializers

    def get_queryset(self):
        queryset = super(MachineList, self).get_queryset()
        request_user = self.request.user
        if not request_user.is_superuser:
            user_department = request_user.department
            department_list = list(user_department.get_all_sub_departments())
            department_list.append(user_department)
            queryset = queryset.filter(department__in=department_list)

        name__contains = self.request.GET.get('name__contains')
        equip_sn__contains = self.request.GET.get('equip_sn__contains')
        cabinet_id = self.request.GET.get('cabinet_id')
        department_id = self.request.GET.get('department_id')
        computer_room_id = self.request.GET.get('computer_room_id')
        machine_id = self.request.GET.get('machine_id')
        if name__contains:
            queryset = queryset.filter(name__contains=name__contains)

        if machine_id:
            queryset = queryset.filter(id=machine_id)

        if equip_sn__contains:
            queryset = queryset.filter(equip_sn__contains=equip_sn__contains)

        if department_id:
            queryset = queryset.filter(department_id=department_id)

        return queryset

    def post(self, request, *args, **kwargs):
        success_msg = '更新成功'

        try:
            post_data =request.data
            name = post_data.get('name')
            description = post_data.get('description')
            equip_model = post_data.get('equip_model')
            equip_type = post_data.get('equip_type')
            equip_sn = post_data.get('equip_sn')
            equip_use = post_data.get('equip_use')
            department_id = post_data.get('department_id')
            cabinet_unit_ids = post_data.get('cabinet_unit_ids')
            u_count = len(cabinet_unit_ids)
            machine = Machine(name=name, description=description, equip_model=equip_model,
                              equip_type=equip_type, equip_sn=equip_sn, equip_use=equip_use,
                              department_id=department_id, u_count=u_count)
            machine.save()

            if not machine_obj.up_to_unit(cabinet_unit_ids):
                success_msg = '该机位(unit)已有设备'

        except Exception as e:
            print(e)
            return Response({'success': False, 'msg': '创建失败'}, status=status.HTTP_200_OK)
        return Response({'success': True, 'msg': success_msg}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def update_machine(request):
    success_msg = '更新成功'
    try:
        post_data = request.data
        machine_id = post_data.get('machine_id')
        name = post_data.get('name')
        equip_model = post_data.get('equip_model')
        equip_type = post_data.get('equip_type')
        equip_sn = post_data.get('equip_sn')
        equip_use = post_data.get('equip_use')
        department_id = post_data.get('department_id')
        cabinet_unit_ids = post_data.get('cabinet_unit_ids')

        machine_obj = Machine.objects.get(id=machine_id)
        machine_obj.name = name
        machine_obj.equip_model = equip_model
        machine_obj.equip_type = equip_type
        machine_obj.equip_sn = equip_sn
        machine_obj.equip_use = equip_use
        machine_obj.department_id = department_id
        machine_obj.save()

        machine_obj.down_from_unit()
        if not machine_obj.up_to_unit(cabinet_unit_ids):
            success_msg = '该机位(unit)已有设备'

    except Exception as e:
        print(e)
        return Response({'success': False, 'msg': '更新失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': success_msg}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_machine(request):
    try:
        machine_id = request.data.get('machine_id')
        machine_obj = Machine.objects.get(id=machine_id)
        machine_obj.deleted = True
        machine_obj.save()
    except Exception as e:
        return Response({'success': False, 'msg': '删除失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '删除成功'}, status=status.HTTP_200_OK)



