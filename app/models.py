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

class Version(models.Model):
    id = models.AutoField(primary_key=True)
    app_id = models.ForeignKey(App)  
    name = models.CharField(max_length=1024, null=False)
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):  
        return self.name


class Patch(models.Model):
    id = models.AutoField(primary_key=True)
    version_id = models.ForeignKey(Version)  
    serial_number = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    desc = models.CharField(max_length=1024, null=False)
    upload_time = models.DateTimeField(auto_now=True)

    def __str__(self):  
        return str(self.serial_number)

class Release(models.Model):
    id = models.AutoField(primary_key=True)
    version_id = models.ForeignKey(Version)  
    patch_id = models.ForeignKey(Patch)  
    is_enable = models.BooleanField()

    def __str__(self):  
        return str(self.id)
