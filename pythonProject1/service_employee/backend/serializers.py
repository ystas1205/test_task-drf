from rest_framework import serializers
from backend.models import Employee, Departament


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'last_name', 'first_name', 'surname', 'photo',
                  'salary', 'age']


class DepartamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departament
        fields = ['id', 'name']
