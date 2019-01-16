from rest_framework import serializers
from equipment.models import Machine


class MachineSerializers(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    cabinet_units = serializers.SerializerMethodField()
    cabinet = serializers.SerializerMethodField()
    computer_room = serializers.SerializerMethodField()

    def get_department_name(self, obj):
        department = obj.department
        if department:
            return department.name
        return None

    def get_cabinet_units(self, obj):
        cabinet_unit = obj.cabinet_units.all()
        cabinet_unit_info = []
        if cabinet_unit:
            for i in cabinet_unit:
                cabinet_unit_info.append({
                    'id': i.id,
                    'name': i.name
                })
            return cabinet_unit_info
        return None

    def get_cabinet(self, obj):
        first_cabinet_unit = obj.cabinet_units.first()
        if first_cabinet_unit :
            cabinet = obj.cabinet_units.first().cabinet
            if cabinet:
                return {'id': cabinet.id, 'name': cabinet.name}
        return None

    def get_computer_room(self, obj):
        first_cabinet_unit = obj.cabinet_units.first()
        if first_cabinet_unit:
            cabinet = obj.cabinet_units.first().cabinet
            if cabinet:
                computer_room = cabinet.computer_room
                if computer_room:
                    return {'id': computer_room.id, 'name': computer_room.name}
        return None

    class Meta:
        model = Machine
        fields = '__all__'
