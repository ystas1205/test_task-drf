from rest_framework import serializers

from backend.models import LoyaltyCard, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_date', 'description',
                  ]


class LoyaltyСardSerializer(serializers.ModelSerializer):
    loyaltycard = TransactionSerializer(read_only=True, many=True)

    class Meta:
        model = LoyaltyCard
        fields = ['id', 'series', 'number', 'issue_date',
                  'expiry_date', 'status', 'loyaltycard']
