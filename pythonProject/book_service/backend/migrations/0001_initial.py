# Generated by Django 5.0.2 on 2024-05-16 17:04

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Название')),
                ('author', models.CharField(max_length=80, verbose_name='Автор')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='Дата выхода')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Список книг',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Ссылка')),
                ('address', models.CharField(max_length=50, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Список магазинов',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50, verbose_name='Город')),
                ('street', models.CharField(max_length=100, verbose_name='Улица')),
                ('house', models.CharField(blank=True, max_length=15, verbose_name='Дом')),
                ('structure', models.CharField(blank=True, max_length=15, verbose_name='Корпус')),
                ('building', models.CharField(blank=True, max_length=15, verbose_name='Строение')),
                ('apartment', models.CharField(blank=True, max_length=15, verbose_name='Квартира')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Контакты пользователя',
                'verbose_name_plural': 'Список контактов пользователя',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Список заказ',
                'ordering': ('-reg_date',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('book', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', to='backend.book', verbose_name='Информация о книге')),
                ('order', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', to='backend.order', verbose_name='Заказ')),
                ('shop', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', to='backend.shop', verbose_name='Информация о магазине')),
            ],
            options={
                'verbose_name': 'Заказанная книга',
                'verbose_name_plural': 'Список заказанных книг',
            },
        ),
    ]
