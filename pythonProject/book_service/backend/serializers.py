
from rest_framework import serializers
from backend.models import Contact, OrderItem, Shop, Order, Book, User
from rest_framework.exceptions import ValidationError


class ContactSerializer(serializers.ModelSerializer):
    """Serializer для контактов пользователя."""
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'building',
                  'apartment', 'user', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {'user': {'write_only': True}, }


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'contacts')
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'address', 'url')
        read_only_fields = ('id',)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name', ' author')
        read_only_fields = ('id',)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'book_quantity', 'book', 'order', 'shop')
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True},

        }


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'reg_date', 'ordered_items')
        read_only_fields = ('id',)
