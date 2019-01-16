from rest_framework import serializers
from users.models import UserProfile, Department


class UserProfileSerializers(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_department_name(self, obj):
        department = obj.department
        if department:
            return department.name
        return None

    class Meta:
        model = UserProfile
        fields = '__all__'


class DepartmentSerializers(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()

    def get_parent_name(self, obj):
        parent = obj.parent
        if parent:
            return parent.name
        return None

    class Meta:
        model = Department
        fields = '__all__'

