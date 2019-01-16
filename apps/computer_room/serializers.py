from rest_framework import serializers
from computer_room.models import ComputerRoom, Cabinet, CabinetUnit


class ComputerRoomSerializers(serializers.ModelSerializer):

    class Meta:
        model = ComputerRoom
        fields = '__all__'


class CabinetSerializers(serializers.ModelSerializer):
    computer_room_name = serializers.SerializerMethodField()
    plan_department_name = serializers.SerializerMethodField()

    def get_computer_room_name(self, obj):
        computer_room = obj.computer_room
        if computer_room:
            return computer_room.name
        return None

    def get_plan_department_name(self, obj):
        plan_department = obj.plan_department
        if plan_department:
            return plan_department.name
        return None

    class Meta:
        model = Cabinet
        fields = '__all__'
        

class CabinetUnitSerializers(serializers.ModelSerializer):
    cabinet_name = serializers.SerializerMethodField()
    plan_department_name = serializers.SerializerMethodField()
    used_department_name = serializers.SerializerMethodField()
    machine_name = serializers.SerializerMethodField()

    def get_cabinet_name(self, obj):
        cabinet = obj.cabinet
        return cabinet.name

    def get_plan_department_name(self, obj):
        plan_department = obj.plan_department
        if plan_department:
            return plan_department.name
        return None

    def get_used_department_name(self, obj):
        used_department = obj.used_department
        if used_department:
            return used_department.name
        return None

    def get_machine_name(self, obj):
        machine = obj.machine
        if machine:
            return machine.name
        return None

    class Meta:
        model = CabinetUnit
        fields = '__all__'