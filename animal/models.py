from django.db import models


class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    sex = models.ForeignKey('Sex', on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=255)
    availability = models.BooleanField()
    description = models.TextField()
    healthy = models.BooleanField()

class AnimalMedia(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    media_link = models.CharField(max_length=255) # edit
    main = models.BooleanField()

class Sex(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    user = models.ForeignKey('user.customuser', on_delete=models.CASCADE)