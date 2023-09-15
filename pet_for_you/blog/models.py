from django.db import models


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    media = models.CharField(max_length=255)
    user_id = models.ForeignKey('user.customuser', on_delete=models.CASCADE)
    animal_id = models.ForeignKey('animal.animal', on_delete=models.CASCADE, null=True)