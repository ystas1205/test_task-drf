from django.urls import path

from backend.views import LoyaltyСardGenerator, Transaction, LoyaltyCardView

app_name = 'backend'

urlpatterns = [
    path('generatorcard', LoyaltyСardGenerator.as_view(),
         name='generatorcard'),
    path('loyaltycard',
         LoyaltyCardView.as_view({"get": "list"}),
         name='loyaltycard'),
    path('loyaltycard/<int:pk>/',
         LoyaltyCardView.as_view({"get": "retrieve", "delete": "destroy",
                                  "patch": "partial_update"})),
    path('transaction',
         Transaction.as_view({"get": "list"}),
         name='transaction'),
]
