import yaml
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.serializers import UserSerializer, ContactSerializer, OrderItemSerializer, OrderSerializer, OrderItem
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from ujson import loads as load_json
from backend.models import Order, Contact, Shop, Book
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterUser(APIView):
    """ Класс для регестрация пользователя"""

    def post(self, request, *args, **kwargs):
        """ Регестрация пользователя"""
        if {'first_name', 'last_name', 'email'}.issubset(request.data):
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                return Response({'status': 'Регистрация прошла успешно'},
                                status=status.HTTP_201_CREATED)
        return Response({'status': 'Не указаны все необходимые аргументы'},
                        status=status.HTTP_400_BAD_REQUEST)


class ContactUser(APIView):
    """ Класс для получения удаление добавление и замены контактных данных """

    def post(self, request, *args, **kwargs):
        """ Добавление контактов """
        if not request.user.is_authenticated:
            return Response({'message': 'Требуется войти'},
                            status=status.HTTP_403_FORBIDDEN)
        count_contact = Contact.objects.filter(user_id=request.user.id).count()
        if count_contact > 0:
            raise ValidationError('У вас уже есть контаткы')
        if {'city', 'street', 'phone'}.issubset(request.data):
            request.data._mutable = True
            request.data.update({'user': request.user.id})
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status': 'Контакты добавлены'},
                                status=status.HTTP_201_CREATED)
        return Response({'Status': 'Не указаны все необходимые аргументы'},
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """ Обновление контактов """
        if not request.user.is_authenticated:
            return Response({'message': 'Требуется войти'},
                            status=status.HTTP_403_FORBIDDEN)

        if 'id' in request.data:
            if request.data['id'].isdigit():
                contact = Contact.objects.filter(id=request.data['id'],
                                                 user_id=request.user.id).first()
                if contact:
                    serializer = ContactSerializer(contact, data=request.data,
                                                   partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response({'status': 'Контакты обновлены'},
                                        status=status.HTTP_201_CREATED)
        return Response({'Status': 'Не указаны все необходимые аргументы'},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """ Удаление контатов """
        if not request.user.is_authenticated:
            return Response({'message': 'Требуется войти'},
                            status=status.HTTP_403_FORBIDDEN)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            query = Q()
            objects_deleted = False
            for contact_id in items_list:
                if contact_id.isdigit():
                    query = query | Q(user_id=request.user.id, id=contact_id)
                    objects_deleted = True
                else:
                    return Response({'message': 'Введены некорректные данные'},
                                    status=status.HTTP_403_FORBIDDEN)
            if objects_deleted:
                deleted_count = Contact.objects.filter(query).delete()[0]
                return Response(
                    {'message': f'Удалено {deleted_count}'},
                    status=status.HTTP_204_NO_CONTENT)
        return Response({'Status': 'Не указаны все необходимые аргументы'},
                        status=status.HTTP_400_BAD_REQUEST)


class UserData(APIView):
    """ Класс получения контактных данных пользователя """

    def get(self, request, *args, **kwargs):
        """ Получения контактных данных пользователя"""
        if not request.user.is_authenticated:
            return Response({'message': 'Требуется войти'},
                            status=status.HTTP_403_FORBIDDEN)
        if 'id' in request.data:
            if request.data['id'].isdigit():
                user_data = User.objects.filter(
                    pk=request.user.id).prefetch_related('contacts')
                serializer = UserSerializer(user_data, many=True)
                return Response(serializer.data)


class OrderView(APIView):
    """ Класс для получения удаление добавление и замены контактных данных """

    def post(self, request, *args, **kwargs):
        """ Добавление заказа """

        if not request.user.is_authenticated:
            return Response({'message': 'Требуется войти'},
                            status=status.HTTP_403_FORBIDDEN)

        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = load_json(items_sting)
            except ValueError:
                return Response({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                order, _ = Order.objects.get_or_create(
                    user_id=request.user.id, state=True)
                order.save()
                objects_created = 0
                for order_item in items_dict:
                    order_item.update({'order': order.id})
                    serializer = OrderItemSerializer(data=order_item)
                    if serializer.is_valid():
                        try:
                            serializer.save()
                        except IntegrityError as error:
                            return Response({'Status': False, 'Errors': str(error)})
                        else:
                            objects_created += 1
                    else:
                        return Response({'Status': False, 'Errors': serializer.errors})
                return Response(
                    {'Status': True,  'Создано объектов': objects_created}, status=status.HTTP_201_CREATED)
        return Response({'Status': False,
                         'Errors': 'Не указаны все необходимые аргументы'})

    def put(self, request, *args, **kwargs):
        """ Изменение заказа """
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = load_json(items_sting)
            except ValueError:
                return Response({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                order, _ = Order.objects.get_or_create(
                    user_id=request.user.id, state=True)
                objects_updated = 0
                for order_item in items_dict:
                    if type(order_item['id']) == int and type(order_item['shop']) == int and type(order_item['book']) == int:
                        objects_updated += OrderItem.objects.filter(
                            order_id=order.id, id=order_item['id']).update(shop_id=order_item['shop'], book_id=order_item['book'], book_quantity=order_item['book_quantity'])
                return Response({'Status': True, 'Обновлено объектов': objects_updated})
        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    def delete(self, request, *args, **kwargs):
        """ Удаление заказа """
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            order, _ = Order.objects.get_or_create(
                user_id=request.user.id, state=True)
            query = Q()
            objects_deleted = False
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    query = query | Q(order_id=order.id, id=order_item_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = OrderItem.objects.filter(query).delete()[0]
                return Response({'Status': True, 'Удалено объектов': deleted_count}, status=status.HTTP_204_NO_CONTENT)
        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class OrderData(APIView):
    """ Класс данных определенного заказа """

    def get(self, request, *args, **kwargs):
        """Получение определенного заказа"""
        if not request.user.is_authenticated:
            return Response({'message': 'Требуется войти'},
                            status=status.HTTP_403_FORBIDDEN)

        if 'id' in request.data:
            if request.data['id'].isdigit():
                order = Order.objects.filter(
                    id=request.data['id']).prefetch_related('ordered_items')

                serializer = OrderSerializer(order, many=True)
                return Response(serializer.data)


class OrderHistory(APIView):
    """ Класс истории заказов пользователя"""

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'Требуется войти'},
                            status=status.HTTP_403_FORBIDDEN)
        orderhistory = Order.objects.filter(
            user_id=request.user.id).prefetch_related('ordered_items')
        serializer = OrderSerializer(orderhistory, many=True)
        return Response(serializer.data)


class Updateproduct(APIView):
    """ Загрузка  данных в файл """

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'Требуется войти'},
                            status=status.HTTP_403_FORBIDDEN)
        data_shop = Shop.objects.all()
        data_book = Book.objects.all()
        list_shop = []
        list_book = []
        for item in data_shop:
            list_shop.append({
                'id': item.id,
                'name': item.name,
                'url': item.url,
                'address': item.address})
        for item_book in data_book:
            list_book.append({
                'id': item_book.id,
                'author': item_book.author,
                'release_date': item_book.release_date,
            })
            data = {'shop': list_shop,
                    'book': list_book}
        with open("prod.yaml", "r+", encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True, sort_keys=False)

            return Response({'message': 'Файл загружен'},
                            status=status.HTTP_403_FORBIDDEN)


class ImportProduct(APIView):
    """ Загруза данных в базу """

    def post(self, request, *args, **kwargs):
        with open('prod.yaml', 'r') as file:
            data = yaml.safe_load(file)
            for i in data['shop']:
                shop_objects, _ = Shop.objects.get_or_create(
                    id=i['id'], name=i['name'], url=i['url'], address=i['address'])
            for item_book in data['book']:
                book_objects, _ = Book.objects.get_or_create(
                    id=item_book['id'], author=item_book['author'], release_date=item_book['release_date'])
            return Response({'message': 'База загружена'},
                            status=status.HTTP_403_FORBIDDEN)
