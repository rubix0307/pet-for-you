from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='Фамилия')

    email = models.EmailField(unique=True)
    media = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return f'<{self.__class__.__name__} - {self.email}'
