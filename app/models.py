from django.db import models

# Create your models here.

class System(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, null=False)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, null=False)
