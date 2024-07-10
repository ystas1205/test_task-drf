import datetime

from django.db import models


# Create your models here.

class TransactionHistory(models.Model):
    objects = models.manager.Manager()

    costumer = models.CharField(max_length=80, verbose_name='Клиент')
    item = models.CharField(max_length=50, verbose_name='Камень')
    total = models.PositiveIntegerField(verbose_name='Сумма')
    quantity = models.IntegerField(verbose_name="Заказы")
    date = models.DateTimeField(verbose_name='Время')

    class Meta:
        # ordering = ['total']
        verbose_name = 'История транзакций'
        verbose_name_plural = "Список истории транзакций"
