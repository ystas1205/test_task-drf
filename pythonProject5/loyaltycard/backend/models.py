import random
from datetime import timedelta
from django.utils import timezone
from django.db import models

STATE_CHOICES = (
    ('not activated', 'Не активирована'),
    ('activated', 'Активирована'),
    ('expired', 'Просрочена'),
)


class LoyaltyCard(models.Model):
    series = models.CharField(max_length=10, verbose_name="Серия карты")
    number = models.CharField(max_length=10, unique=True,
                              verbose_name="Номер карты")
    issue_date = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата выпуска карты")
    expiry_date = models.DateTimeField(
        verbose_name="Дата истичения срока карты")

    status = models.CharField(max_length=20, choices=STATE_CHOICES,
                              default='activated')

    class Meta:
        verbose_name = 'Дисконтная карта'
        verbose_name_plural = "Список дисконтных карт"

    @staticmethod
    def generate_card_number():
        """Генерирует уникальный номер карты."""
        return f"{''.join([str(random.randint(0, 9)) for _ in range(8)])}"

    @classmethod
    def generate_cards(cls, series, quantity):
        """Генерирует карты с указанными параметрами."""

        validity_period = {
            365: "1year",
            182: "6months",
            31: "1months",
        }
        cards_to_create = []
        for _ in range(quantity):
            # генерирует номер карты
            card_number = cls.generate_card_number()
            # генерирует срок действия карты
            expiry_date = timezone.now() + timedelta(
                days=random.choice(list(validity_period)))

            card = cls(series=series, number=card_number,
                       expiry_date=expiry_date)
            cards_to_create.append(card)
        cls.objects.bulk_create(cards_to_create)


class Transaction(models.Model):
    loyalty_card = models.ForeignKey('LoyaltyCard', on_delete=models.CASCADE,
                                     related_name='loyaltycard')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True,
                                            verbose_name="Дата использованиня карты")
    description = models.TextField()

    class Meta:
        verbose_name = 'Транзакция карты'
        verbose_name_plural = "Список транзакций карт"

    def __str__(self):
        return f"Покупка {self.amount} на карте {LoyaltyCard.number}"
