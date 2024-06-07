

from typing import Type

from django.dispatch import receiver,Signal
from django.db.models.signals import post_save
from requests import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from backend.models import User



@receiver(post_save, sender=User)
def new_user_registered_signal(sender: Type[User], instance: User,
                               created: bool, **kwargs):
    """ Отправляем письмо с подтрердждением почты """

    if created and instance.is_active:
        token = Token.objects.get_or_create(user_id=instance.pk)
       
        
