from django.db.models import Sum, Count
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from backend.models import Employee, Departament
from backend.serializers import EmployeeSerializer, DepartamentSerializer


class EmployeeViewSet(ModelViewSet):
    """ Класс для получение, удаление и изменение данных сотрудника"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['last_name']
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]


class DepartamentViewSet(ModelViewSet):
    queryset = Departament.objects.all()
    serializer_class = DepartamentSerializer


    def list(self, request, *args, **kwargs):
        """ API для получения списка департаментов (включает искусственное поле
         с числом сотрудников + поле с суммарным окладам по всем сотрудникам)"""
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {'result': response.data}
        response_data['total_salary'] = queryset.aggregate(
            total=Sum('employee__salary')).get('total')
        response_data['number_employee'] = queryset.aggregate(
            total=Count('employee')).get('total')
        response.data = response_data
        return response
