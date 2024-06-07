from django.db import models


# Create your models here.
class Employee(models.Model):
    objects = models.manager.Manager()
    last_name = models.CharField(max_length=50, db_index=True,
                                 verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Имя')
    photo = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True,
                              null=True, verbose_name="Фото")
    salary = models.PositiveIntegerField(verbose_name='Оклад')
    age = models.PositiveIntegerField(verbose_name='Возраст')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.surname}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = "Список сотрудников"


class Departament(models.Model):
    objects = models.manager.Manager()
    name = models.CharField(max_length=120, unique=True,
                            verbose_name='Название')
    employee = models.OneToOneField(Employee, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='departament',
                                    verbose_name='Сотрудник')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = "Список департаментов"
