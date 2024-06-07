from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)


class Book(models.Model):
    objects = models.manager.Manager()
    name = models.CharField(max_length=80, verbose_name='Название')
    author = models.CharField(max_length=80, verbose_name="Автор")
    release_date = models.DateField(
        verbose_name='Дата выхода', blank=True, null=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = "Список книг"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Shop(models.Model):
    objects = models.manager.Manager()
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name="Адрес")

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Order(models.Model):
    objects = models.manager.Manager()
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='orders',
                             on_delete=models.CASCADE)
    reg_date = models.DateTimeField(
        auto_now=True, verbose_name='Время заказа')
    state = models.BooleanField(verbose_name='Статус получения заказа',
                                default=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказ"
        ordering = ('-reg_date',)

    def __str__(self):
        return str(self.reg_date)


class Contact(models.Model):
    objects = models.manager.Manager()
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='contacts',
                             on_delete=models.CASCADE)

    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Корпус',
                                 blank=True)
    building = models.CharField(max_length=15, verbose_name='Строение',
                                blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира',
                                 blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = "Список контактов пользователя"

    def __str__(self):
        return f'{self.city} {self.street} {self.house}'


class OrderItem(models.Model):
    objects = models.manager.Manager()
    order = models.ForeignKey(Order, verbose_name='Заказ',
                              related_name='ordered_items', blank=True,
                              on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Информация о магазине',
                             related_name='ordered_items',
                             blank=True,
                             on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='Информация о книге',
                             related_name='ordered_items',
                             blank=True,
                             on_delete=models.CASCADE)
    book_quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказанная книга'
        verbose_name_plural = "Список заказанных книг"
