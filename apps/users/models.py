from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    """
    组织架构
    """
    name = models.CharField(max_length=20, unique=True)
    parent = models.ForeignKey("self",
                               on_delete=models.SET_NULL,
                               related_name='sub_departments',
                               blank=True,
                               null=True)

    def get_all_sub_departments(self):
        sub_dps = self.sub_departments.all()
        for sub_dp in sub_dps:
            sub_dps = sub_dps | sub_dp.get_all_sub_departments()
        return sub_dps

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    """
    用户: makemigration提示错误：sers.UserProfile.user_permissions: (fields.E304)，
    需要在settings中指定自定义认证模型：AUTH_USER_MODEL = 'users.UserProfile'
    """
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10,
                              choices=(
                                  ('1', "male"),
                                  ('2', "female")
                              ),
                              default='1')
    mobile = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department,
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='user_department')
    post = models.CharField(max_length=50, null=True, blank=True)
    joined_date = models.DateField(null=True, blank=True)
    ID_number = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

