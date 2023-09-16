from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    media = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фото')

    REQUIRED_FIELDS = ['first_name', 'last_name','email', 'phone']

    def __str__(self):
        return self.email