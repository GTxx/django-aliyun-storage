from django.db import models

# Create your models here.

class Student(models.Model):
    avatar = models.ImageField()
    name = models.CharField(max_length=16)