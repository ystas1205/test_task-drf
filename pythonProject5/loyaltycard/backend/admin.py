from django.contrib import admin

from backend.models import LoyaltyCard, Transaction


# Register your models here.


@admin.register(LoyaltyCard)
class LoyaltyCardAdmin(admin.ModelAdmin):
    list_display = ['id', 'series', 'number', 'issue_date',
                    'expiry_date', 'status']
    list_display_links = ['id', 'series']
    list_per_page = 15


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'transaction_date', 'description',
                    ]
    list_display_links = ['id', 'amount']
    list_per_page = 15
