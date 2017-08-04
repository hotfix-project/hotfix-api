from django.db import models

# Create your models here.

class System(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, null=False)

    def __str__(self):  
        return self.name

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, null=False)
  
    def __str__(self):  
        return self.name

class App(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category)  
    system_id = models.ForeignKey(System)  
    name = models.CharField(max_length=1024, null=False)
    key = models.CharField(max_length=1024, null=False)
    secret = models.CharField(max_length=1024, null=False)
    rsa = models.CharField(max_length=1024, null=False)

    def __str__(self):  
        return self.name
