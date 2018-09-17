from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField('name',max_length=64)