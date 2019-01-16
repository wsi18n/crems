from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import UserProfile, Department


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'gender', 'mobile', 'email',
                    'department', 'joined_date')
    list_filter = ('created_at',)
    search_fields = ('id',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'leader', 'parent')
    list_filter = ('created_at',)
    search_fields = ('name',)


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Department)