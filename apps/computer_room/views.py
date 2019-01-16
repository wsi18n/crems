# coding=utf-8
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from computer_room.models import ComputerRoom, Cabinet, CabinetUnit
from computer_room.serializers import ComputerRoomSerializers, CabinetSerializers, CabinetUnitSerializers
from equipment.models import Machine
from users.models import Department, UserProfile


class ComputerRoomList(generics.ListAPIView):
    queryset = ComputerRoom.objects.filter(deleted=False)
    serializer_class = ComputerRoomSerializers

    def get_queryset(self):
        queryset = super(ComputerRoomList, self).get_queryset()
        computer_room_id = self.request.GET.get('computer_room_id')
        name__contains = self.request.GET.get('name__contains')
        address__contains = self.request.GET.get('address__contains')

        if computer_room_id:
          queryset = queryset.filter(id=computer_room_id)
        if name__contains:
            queryset = queryset.filter(name__contains=name__contains)
        if address__contains:
            queryset = queryset.filter(address__contains=address__contains)
        return queryset

    def post(self, request, *args, **kwargs):
        try:
            post_data =request.data
            name = post_data.get('name')
            description = post_data.get('description')
            address = post_data.get('address', '')
            ComputerRoom.objects.create(name=name, description=description, address=address)
        except Exception as e:
            return Response({'success': False, 'msg': '创建失败'}, status=status.HTTP_200_OK)
        return Response({'success': True, 'msg': '创建成功'}, status=status.HTTP_200_OK)


class CabinetList(generics.ListAPIView):
    queryset = Cabinet.objects.filter(deleted=False)
    serializer_class = CabinetSerializers

    def get_queryset(self):
        queryset = super(CabinetList, self).get_queryset()
        request_user = self.request.user
        if not request_user.is_superuser:
            user_department = request_user.department
            department_list = list(user_department.get_all_sub_departments())
            department_list.append(user_department)
            queryset = queryset.filter(plan_department__in=department_list)

        cabinet_id = self.request.GET.get('cabinet_id')
        computer_room_id = self.request.GET.get('computer_room_id')
        name__contains = self.request.GET.get('name__contains')
        if cabinet_id:
            queryset = queryset.filter(id=cabinet_id)
        if computer_room_id:
            queryset = queryset.filter(computer_room_id=computer_room_id)
        if name__contains:
            queryset = queryset.filter(name__contains=name__contains)
        return queryset

    def post(self, request, *args, **kwargs):
        try:
            post_data =request.data
            name = post_data.get('name')
            description = post_data.get('description')
            total_unit_number = post_data.get('total_unit_number')
            cabinet_row = post_data.get('cabinet_row')
            cabinet_col = post_data.get('cabinet_col')
            computer_room_id = post_data.get('computer_room_id')
            plan_department_id = post_data.get('plan_department_id')
            plan_department_obj = Department.objects.get(id=plan_department_id)
            computer_room_obj = ComputerRoom.objects.get(id=computer_room_id)
            cabinet_obj = Cabinet.objects.create(name=name, description=description, total_unit_number=total_unit_number,
                                          available_unit_number=total_unit_number, cabinet_row=cabinet_row,
                                          cabinet_col=cabinet_col, computer_room=computer_room_obj,
                                          plan_department=plan_department_obj, used_department=plan_department_obj)
            if total_unit_number:
                for i in range(int(total_unit_number)):
                    cabinet_unit_name = str(cabinet_row) + str(cabinet_col) + '-' + str(i+1)
                    CabinetUnit.objects.create(name=cabinet_unit_name, cabinet=cabinet_obj,
                                               plan_department=plan_department_obj)


        except Exception as e:
            print(e)
            return Response({'success': False, 'msg': '创建失败'}, status=status.HTTP_200_OK)
        return Response({'success': True, 'msg': '创建成功'}, status=status.HTTP_200_OK)


class CabinetUnitList(generics.ListAPIView):
    queryset = CabinetUnit.objects.filter(deleted=False)
    serializer_class = CabinetUnitSerializers

    def get_queryset(self):
        queryset = super(CabinetUnitList, self).get_queryset()
        request_user = self.request.user
        if not request_user.is_superuser:
            user_department = request_user.department
            department_list = list(user_department.get_all_sub_departments())
            department_list.append(user_department)
            queryset = queryset.filter(plan_department__in=department_list)

        cabinet_unit_id = self.request.GET.get('cabinet_unit_id')
        cabinet_id = self.request.GET.get('cabinet_id')
        if cabinet_id:
            queryset = queryset.filter(cabinet_id=cabinet_id)
        if cabinet_unit_id:
            queryset = queryset.filter(id=cabinet_unit_id)
        return queryset

    def post(self, request, *args, **kwargs):
        try:
            post_data =request.data
            name = post_data.get('name')
            description = post_data.get('description')
            cabinet_id = post_data.get('cabinet_id')
            plan_department_id = post_data.get('plan_department_id')
            state = post_data.get('state')
            machine_id = post_data.get('machine_id')
            cabinet_obj = Cabinet.objects.get(id=cabinet_id)
            plan_department_obj = Department.objects.get(id=plan_department_id)
            machine_obj = Machine.objects.get(id=machine_id)

            CabinetUnit.objects.create(name=name, description=description, cabinet=cabinet_obj,
                                       plan_department=plan_department_obj, machine=machine_obj, state=state)
        except Exception as e:
            return Response({'success': False, 'msg': '创建失败'}, status=status.HTTP_200_OK)
        return Response({'success': True, 'msg': '创建成功'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_computer_room(request):
    try:
        computer_room_id = request.data.get('computer_room_id')
        computer_room_obj = ComputerRoom.objects.get(id=computer_room_id)
        computer_room_obj.deleted = True
        computer_room_obj.save()
        cabinet = Cabinet.objects.filter(computer_room_id=computer_room_id)
        for i in cabinet:
            i.deleted = True
            i.save()
    except Exception as e:
        return Response({'success': False, 'msg': '删除失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '删除成功'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_cabinet(request):
    try:
        cabinet_id = request.data.get('cabinet_id')
        cabinet_obj = Cabinet.objects.get(id=cabinet_id)
        cabinet_obj.deleted = True
        cabinet_obj.save()
        cabinet_unit = CabinetUnit.objects.filter(cabinet_id=cabinet_id)
        for i in cabinet_unit:
            i.deleted = True
            i.save()
    except Exception as e:
        return Response({'success': False, 'msg': '删除失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '删除成功'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_cabinet_unit(request):
    try:
        cabinet_unit_id = request.data.get('cabinet_unit_id')
        cabinet_unit_obj = CabinetUnit.objects.get(id=cabinet_unit_id)
        cabinet_unit_obj.deleted = True
        cabinet_unit_obj.save()
    except Exception as e:
        return Response({'success': False, 'msg': '删除失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '删除成功'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def update_computer_room(request):
    try:
        post_data = request.data
        computer_room_id = post_data.get('computer_room_id')
        name = post_data.get('name')
        description = post_data.get('description')
        address = post_data.get('address', '')

        computer_room_obj = ComputerRoom.objects.get(id=computer_room_id)
        computer_room_obj.name = name
        computer_room_obj.description = description
        computer_room_obj.address = address
        computer_room_obj.save()
    except Exception as e:
        print(e)
        return Response({'success': False, 'msg': '更新失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '更新成功'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def update_cabinet(request):
    try:
        post_data = request.data
        cabinet_id = post_data.get('cabinet_id')
        name = post_data.get('name')
        description = post_data.get('description')
        total_unit_number = post_data.get('total_unit_number')
        cabinet_row = post_data.get('cabinet_row')
        cabinet_col = post_data.get('cabinet_col')
        computer_room_id = post_data.get('computer_room_id')
        plan_department_id = post_data.get('plan_department_id')
        plan_department_obj = Department.objects.get(id=plan_department_id)
        computer_room_obj = ComputerRoom.objects.get(id=computer_room_id)

        cabinet_obj = Cabinet.objects.get(id=cabinet_id)
        cabinet_obj.name = name
        cabinet_obj.description = description
        cabinet_obj.total_unit_number = total_unit_number
        cabinet_obj.cabinet_row = cabinet_row
        cabinet_obj.cabinet_col = cabinet_col
        cabinet_obj.plan_department = plan_department_obj
        cabinet_obj.computer_room = computer_room_obj
        cabinet_obj.save()
    except Exception as e:
        print(e)
        return Response({'success': False, 'msg': '更新失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '更新成功'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def update_cabinet_unit(request):
    try:
        post_data = request.data
        cabinet_unit_id = post_data.get('cabinet_unit_id')
        name = post_data.get('name')
        description = post_data.get('description')
        cabinet_id = post_data.get('cabinet_id')
        plan_department_id = post_data.get('plan_department_id')
        state = post_data.get('state')
        machine_id = post_data.get('machine_id')
        cabinet_obj = Cabinet.objects.get(id=cabinet_id)
        plan_department_obj = Department.objects.get(id=plan_department_id)
        machine_obj = Machine.objects.get(id=machine_id)

        cabinet_unit_obj = CabinetUnit.objects.get(id=cabinet_unit_id)
        cabinet_unit_obj.name = name
        cabinet_unit_obj.description = description
        cabinet_unit_obj.cabinet = cabinet_obj
        cabinet_unit_obj.state = state
        cabinet_unit_obj.plan_department = plan_department_obj
        cabinet_unit_obj.machine = machine_obj
        cabinet_unit_obj.save()
    except Exception as e:
        return Response({'success': False, 'msg': '更新失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '更新成功'}, status=status.HTTP_200_OK)
