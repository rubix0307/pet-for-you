from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    media = models.CharField(max_length=255) # edit