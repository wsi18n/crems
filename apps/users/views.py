# coding=utf-8
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from users.models import UserProfile, Department
from users.serializers import UserProfileSerializers, DepartmentSerializers


class UserProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers

    def get_queryset(self):
        queryset = super(UserProfileList, self).get_queryset()
        user_id = self.request.GET.get('user_id')
        department_id = self.request.GET.get('department_id')
        username__contains = self.request.GET.get('username__contains')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        if username__contains:
            queryset = queryset.filter(username__contains=username__contains)
        if user_id:
            queryset = queryset.filter(id=user_id)
        return queryset

    def post(self, request, *args, **kwargs):
        try:
            post_data =request.data
            username = post_data.get('username')
            password = post_data.get('password')
            first_name = post_data.get('first_name')
            last_name = post_data.get('last_name')
            department_id = post_data.get('department_id')
            ID_number = post_data.get('ID_number')
            mobile = post_data.get('mobile')
            email = post_data.get('email')
            department_obj = Department.objects.get(id=department_id)
            user = UserProfile.objects.create(username=username, first_name=first_name, last_name=last_name,
                                              department=department_obj, ID_number=ID_number, mobile=mobile,
                                              email=email)
            user.set_password(password)
            user.save()
        except Exception as e:
            print(e)
            return Response({'success': False, 'msg': '创建失败'}, status=status.HTTP_200_OK)
        return Response({'success': True, 'msg': '创建成功'}, status=status.HTTP_200_OK)


class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializers

    def get_queryset(self):
        queryset = super(DepartmentList, self).get_queryset()
        parent_id = self.request.GET.get('parent_id')
        department_id = self.request.GET.get('department_id')
        name__contains = self.request.GET.get('name__contains')
        if department_id:
            queryset = queryset.filter(id=department_id)
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        if name__contains:
            queryset = queryset.filter(name__contains=name__contains)
        return  queryset

    def post(self, request, *args, **kwargs):
        try:
            post_data =request.data
            name = post_data.get('name')
            parent_id = post_data.get('parent_id')
            department_obj = Department.objects.get(id=parent_id)
            Department.objects.create(name=name, parent=department_obj)
        except Exception as e:
            return Response({'success': False, 'msg': '创建失败'}, status=status.HTTP_200_OK)
        return Response({'success': True, 'msg': '创建成功'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_user(request):
    try:
        user_id = request.data.get('user_id')
        UserProfile.objects.get(id=user_id).delete()
    except Exception as e:
        return Response({'success': False, 'msg': '删除失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '删除成功'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_department(request):
    try:
        department_id = request.data.get('department_id')
        Department.objects.get(id=department_id).delete()
    except Exception as e:
        return Response({'success': False, 'msg': '删除失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '删除成功'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def update_user(request):
    try:
        post_data = request.data
        user_id = post_data.get('user_id')
        username = post_data.get('username')
        first_name = post_data.get('first_name')
        last_name = post_data.get('last_name')
        mobile = post_data.get('mobile')
        password = post_data.get('password')
        ID_number = post_data.get('ID_number')
        email = post_data.get('email')
        department_id = post_data.get('department_id')

        user = UserProfile.objects.get(id=user_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.mobile = mobile
        user.ID_number = ID_number
        user.email = email
        user.department_id = department_id
        user.set_password(password)
        user.save()
    except Exception as e:
        return Response({'success': False, 'msg': '更新失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '更新成功'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def update_department(request):
    try:
        post_data = request.data
        department_id = post_data.get('department_id')
        name = post_data.get('name')
        parent_id = post_data.get('parent_id')

        department_obj = Department.objects.get(id=department_id)
        department_obj.name = name
        department_obj.parent_id = parent_id
        department_obj.save()
    except Exception as e:
        return Response({'success': False, 'msg': '更新失败'}, status=status.HTTP_200_OK)
    return Response({'success': True, 'msg': '更新成功'}, status=status.HTTP_200_OK)
