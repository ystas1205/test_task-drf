import csv
import io
import operator
from django.core.exceptions import EmptyResultSet, ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import Sum, Max, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import TransactionHistory


# Create your views here.


class ImportProduct(APIView):

    def post(self, request, *args, **kwargs, ):

        file = request.FILES.get('file')
        if not file:
            return JsonResponse({
                'Status': 'Error, Файл не поступил-в процессе обработки файла'
                          ' произошла ошибка.'})
        if file:

            file_wrapper = io.TextIOWrapper(file, encoding='utf-8')
            reader = csv.DictReader(file_wrapper)
            for row in list(reader):
                transaction_object, _ = TransactionHistory.objects.get_or_create(
                    costumer=row['customer'],
                    item=row['item'],
                    total=row['total'],
                    quantity=row['quantity'],
                    date=row['date'])

            return JsonResponse(
                {'Status': 'Ok- файл был обработан без ошибок'})

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):

        queryset = TransactionHistory.objects.order_by('-total')
        dict_costumer_total = {}
        list_item = []
        for data in queryset:
            if data.costumer in dict_costumer_total:
                continue
            dict_costumer_total.update({data.costumer: data.total})
            list_item.append(data.item)
        list_top = (list(dict_costumer_total.items())[:5])
        list_item = list_item[:5]
        list_top_costumer = []
        list_top_item = []
        for costumer, total in list_top:
            for items in list_item:
                if list_item.count(
                        items) > 1 and items not in list_top_item:
                    list_top_item.append(items)
            list_top_costumer.append(
                {"username": costumer, "spent_money": total,
                 'gems': list_top_item})
        response_data = {"response": list_top_costumer}

        return Response(response_data)
