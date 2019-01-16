from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ticket.models import TicketRecord, TicketCustomField
from ticket.serializers import TicketRecordSerializers
from workflow.models import Workflow, State, Transition, CustomField
from equipment.models import Machine
from computer_room import models as computer_room_m

import json

class TicketRecordList(generics.ListAPIView):
    queryset = TicketRecord.objects.filter(deleted=False)
    serializer_class = TicketRecordSerializers

    def get_queryset(self):
        queryset = super(TicketRecordList, self).get_queryset()
        category = self.request.GET.get('category')
        ticket_id = self.request.GET.get('ticket_id')
        if category == 'owner':
            queryset = queryset.filter(creator=self.request.user)

        if category == 'duty':
            queryset = queryset.filter(participant=self.request.user)

        if category == 'relation':
            queryset = queryset.filter(related_user=self.request.user)

        if ticket_id:
            queryset = queryset.filter(id=ticket_id)
        return queryset

    def post(self, request, *args, **kwargs):
        # system_name = request.data.get('name')
        try:
            request_data = request.data
            workflow_id = request_data.get('workflow_id')
            user = request.user
            ticket_sn = gen_ticket_sn()
            ticket_title = request_data.get('ticket_title', '')
            init_state_obj = State.objects.filter(workflow_id=workflow_id, deleted=False, state_type='2').first()
            destination_state = Transition.objects.get(deleted=False, from_state_id=init_state_obj.id).to_state

            new_ticket_obj = TicketRecord(sn=ticket_sn, title=ticket_title, workflow_id=workflow_id,
                                          current_state_id=destination_state.id,
                                          participant_type=destination_state.participant_type,
                                          participant=destination_state.participant,
                                          creator=user, is_end=False
                                          )
            new_ticket_obj.save()
            new_ticket_obj.related_user.add(user, destination_state.participant)

            custom_filed_list = CustomField.objects.filter(deleted=False,
                                                           workflow_id=workflow_id
                                                           )
            for custom_filed in custom_filed_list:
                if request_data.get(custom_filed.field_key, ''):
                    TicketCustomField.objects.create(
                        ticket_record_id=new_ticket_obj.id,
                        name=custom_filed.field_name,
                        field_key=custom_filed.field_key,
                        char_value=request_data.get(custom_filed.field_key, ''),
                    )

        except Exception as e:
            print(e)
            return Response({'success': False, 'msg': '创建失败'}, status=status.HTTP_200_OK)
        return Response({'success': True, 'msg': '创建成功'}, status=status.HTTP_200_OK)


def gen_ticket_sn():
    import datetime
    today = datetime.datetime.now()
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    today_ticket_count = TicketRecord.objects.filter(created_at__range=(today_min, today_max)).count()
    new_ticket_count = int(today_ticket_count) + 1
    return '%04d%02d%02d%04d' % (today.year, today.month, today.day, new_ticket_count)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_ticket_flow_steps(request):
    ticket_id = request.GET.get('ticket_id')
    workflow = TicketRecord.objects.get(id=ticket_id).workflow
    state_queryset = workflow.state_workflow.all()
    ticket_flow_steps = []
    for state in state_queryset:
        ticket_flow_steps.append({
            'state_id': state.id,
            'state_name': state.name,
            'order_id': state.order_id,
        })
    return JsonResponse({'ticket_flow_steps': ticket_flow_steps})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_ticket_transitions(request):
    user = request.user
    ticket_id = request.GET.get('ticket_id')
    participant = TicketRecord.objects.get(id=ticket_id).participant
    if user != participant:
        return JsonResponse({'has_perm': False, 'transitions':''})
    current_state = TicketRecord.objects.get(id=ticket_id).current_state
    transition_objs = current_state.transitions_from.all()
    transitions = []
    for transition in transition_objs:
        transitions.append({
            'id': transition.id,
            'name': transition.name
        })

    return JsonResponse({'has_perm': True, 'transitions': transitions})




@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_ticket_custom_fields(request):
    def get_char_value_describe(obj):
      if obj.field_key == 'equip_position' and obj.char_value:
        cabinet_unit_ids =  json.loads(obj.char_value.replace('\'','\"'))  #json.loads 不支持单引号修饰属性的值!
        cabinet_units = computer_room_m.CabinetUnit.objects.filter(deleted=False, id__in=cabinet_unit_ids)
        cabinet = cabinet_units[0].cabinet
        computer_room = cabinet.computer_room
        return '%s > %s > %s' % (computer_room.name, cabinet.name,', '.join([unit.name for unit in cabinet_units]))

      return obj.char_value

    ticket_id = request.GET.get('ticket_id')
    custom_field_queryset = TicketCustomField.objects.filter(ticket_record_id=ticket_id)
    custom_fields = []

    for custom_field in custom_field_queryset:
        custom_fields.append({
            'id': custom_field.id,
            'name': custom_field.name,
            'char_value': custom_field.char_value,
            'char_value_describe': get_char_value_describe(custom_field),
            'ticket_record': custom_field.ticket_record_id,
            'field_key': custom_field.field_key,
        })
    return JsonResponse({'custom_fields': custom_fields})


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def handle_ticket_state(request):
    success_msg='工单处理成功'
    try:
        request_data = request.data
        ticket_id = request_data.get('ticket_id')
        ticket_obj = TicketRecord.objects.get(id=ticket_id, deleted=False)
        transition_id = request_data.get('transition_id')
        transition_obj = Transition.objects.get(id=transition_id)
        to_state = transition_obj.to_state
        if transition_obj.transition_type == '1':#同意
            if to_state.state_type == '3':#end 完成
                ticket_obj.is_end = True
                ticket_obj.current_state = to_state
                ticket_obj.participant = None
                custom_fields = ticket_obj.ticketcustomfield_set.all()
                custom_fields_dict = {item.field_key: item.char_value for item in custom_fields}

                if ticket_obj.workflow.id ==1 and custom_fields : #上架
                    machine_params ={'department_id':ticket_obj.creator.department.id}
                    if 'equip_in_reason' in custom_fields_dict:
                        machine_params['description'] = custom_fields_dict['equip_in_reason']

                    if 'equip_use' in custom_fields_dict :
                        machine_params['equip_use'] = custom_fields_dict['equip_use']
                    if 'equip_version' in custom_fields_dict:
                        machine_params['equip_version'] = custom_fields_dict['equip_version']
                    if 'equip_type' in custom_fields_dict:
                        machine_params['equip_type'] = custom_fields_dict['equip_type']
                    if 'equip_sn' in custom_fields_dict:
                        machine_params['equip_sn'] = custom_fields_dict['equip_sn']
                    if 'equip_name' in custom_fields_dict:
                        machine_params['name'] = custom_fields_dict['equip_name']

                    machine_params['name'] = 'name' in machine_params and machine_params['name'] or \
                                             'equip_sn' in machine_params and machine_params['equip_sn'] or \
                                             'Unknown'
                    machine_count = Machine.objects.filter(equip_sn=machine_params['equip_sn']).count()
                    if machine_count : #已存在该S/N的设备
                       machine_obj = Machine.objects.filter(equip_sn=machine_params['equip_sn'])[0]
                    else :
                       machine_obj = Machine.objects.create(**machine_params)

                    if 'equip_position' in custom_fields_dict:
                        unit_ids = json.loads(custom_fields_dict['equip_position'].replace('\'', '\"'))
                        machine_obj.up_to_unit(unit_ids)
                    else :
                        success_msg = '工单处理成功，工单未填写机位，请管理员手动填写机位信息'
                if ticket_obj.workflow.id == 2 and custom_fields:  # 下架
                    if 'equip_sn' in custom_fields_dict:
                        equip_sn = custom_fields_dict['equip_sn']
                        machine_count = Machine.objects.filter(equip_sn=equip_sn).count()
                        if machine_count>1:
                            success_msg = '工单处理成功，但多台设备S/N重复，请管理员手动下架设备'
                        if machine_count == 0:
                            success_msg = '工单处理成功，但未查询到对应S/N的设备'
                        else :
                            machine_obj = Machine.objects.filter(equip_sn=equip_sn)[0]
                            machine_obj.down_from_unit()
                    else :
                        return Response({'success': False, 'msg': '处理失败，工单未填写设备S/N'}, status=status.HTTP_200_OK)

                if ticket_obj.workflow.id == 3 and custom_fields:  # 变更
                    if 'equip_sn' in custom_fields_dict and 'equip_position' in custom_fields_dict:
                        equip_sn = custom_fields_dict['equip_sn']
                        machine_count = Machine.objects.filter(equip_sn=equip_sn).count()
                        if machine_count>1:
                            success_msg = '工单处理成功，但多台设备S/N重复，请管理员手动变更设备位置'
                        if machine_count == 0:
                            success_msg = '工单处理成功，但未查询到对应S/N的设备'
                        else :
                            unit_ids = json.loads(custom_fields_dict['equip_position'].replace('\'', '\"'))
                            machine_obj = Machine.objects.filter(equip_sn=equip_sn)[0]
                            machine_obj.down_from_unit()
                            machine_obj.up_to_unit(unit_ids)

                    else :
                        return Response({'success': False, 'msg': '处理失败，工单未填写设备S/N 或 目标机位'}, status=status.HTTP_200_OK)
            else:
                ticket_obj.current_state = to_state
                ticket_obj.participant = to_state.participant
                if to_state.participant:
                    ticket_obj.related_user.add(to_state.participant)
        if transition_obj.transition_type == '2':#拒绝
            ticket_obj.is_rejected = True
            ticket_obj.participant = None

        ticket_obj.save()
    except Exception as e:
        print(e)
        return Response({'success': False, 'msg': '处理失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': success_msg}, status=status.HTTP_200_OK)
