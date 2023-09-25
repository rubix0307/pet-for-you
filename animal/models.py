from django.db import models


class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    type = models.ForeignKey('AnimalType', on_delete=models.CASCADE)
    sex = models.ForeignKey('Sex', on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=255)
    availability = models.BooleanField()
    description = models.TextField()
    healthy = models.BooleanField()

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'

class AnimalMedia(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    media_link = models.CharField(max_length=255)  # edit
    main = models.BooleanField()

    def __str__(self):
        return self.animal

    class Meta:
        verbose_name = 'Медиа животного'
        verbose_name_plural = 'Медиа животных'

class Sex(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

class AnimalType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    user = models.ForeignKey('user.customuser', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    media = models.CharField(max_length=255, null=True)
    user = models.ForeignKey('user.customuser', on_delete=models.CASCADE)
    animal = models.ForeignKey('animal.animal', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'