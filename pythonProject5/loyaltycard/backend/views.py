from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveDestroyAPIView, ListAPIView, \
    DestroyAPIView
from rest_framework.request import Request

from rest_framework.views import APIView

from backend.models import LoyaltyCard, Transaction
from rest_framework.viewsets import ModelViewSet

from backend.serializers import LoyaltyСardSerializer, TransactionSerializer
from filters import LoyaltyCardFilter


# Create your views here.
class LoyaltyСardGenerator(APIView):

    def post(self, request: Request, *args, **kwargs):
        # проверяем обязательные аргументы
        if {'series', 'quantity'}.issubset(request.data):
            LoyaltyCard.generate_cards(request.data['series'],
                                       int(request.data['quantity'],
                                           ))
            # если истек срок обновляется карта
            update_card = LoyaltyCard.objects.filter(
                expiry_date__lt=timezone.now(),
                status='активирована').update(
                status='Просрочена')

            return JsonResponse(
                {
                    'status': f"Добавлено {request.data['quantity']} карт,"
                              f"обновлено {update_card} карт"},
                status=status.HTTP_201_CREATED)
        return JsonResponse({'Status': 'Не указаны все необходимые аргументы'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoyaltyCardView(ModelViewSet):
    queryset = LoyaltyCard.objects.all()
    serializer_class = LoyaltyСardSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', ]
    search_fields = ['series', 'number', 'status', ]
    filterset_class = LoyaltyCardFilter


class Transaction(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
