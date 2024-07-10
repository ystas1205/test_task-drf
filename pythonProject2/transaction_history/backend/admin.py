from django.contrib import admin

from backend.models import TransactionHistory


# Register your models here.


@admin.register(TransactionHistory)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['costumer', 'item', 'total', 'quantity', 'date']
