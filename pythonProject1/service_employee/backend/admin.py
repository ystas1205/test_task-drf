from django.contrib import admin

from backend.models import Employee, Departament


# Register your models here.


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'surname', 'photo',
                    'salary', 'age']
    list_display_links = ['id', 'last_name']
    list_per_page = 15


@admin.register(Departament)
class DepartamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'employee']
    list_display_links = ['name', ]
