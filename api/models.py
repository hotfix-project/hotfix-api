from django.db import models
import datetime

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
    download_url = models.FileField(upload_to='./upload/', blank=True)

    def __str__(self):  
        return str(self.serial_number)

class Release(models.Model):
    id = models.AutoField(primary_key=True)
    patch_id = models.ForeignKey(Patch)  
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(default=datetime.datetime.now)
    download_count = models.IntegerField(default=0)
    apply_count = models.IntegerField(default=0)
    is_enable = models.BooleanField(default=False)
    is_gray = models.BooleanField(default=False)
    pool_size = models.IntegerField(default=0)

    def __str__(self):  
        return str(self.id)
