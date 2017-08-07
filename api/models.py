from django.db import models
from django.db.models import Max
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
    rsa = models.TextField(null=False)

    def __str__(self):  
        return self.name


class Version(models.Model):
    id = models.AutoField(primary_key=True)
    app_id = models.ForeignKey(App)  
    name = models.CharField(max_length=1024, null=False)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.name


class Patch(models.Model):
    id = models.AutoField(primary_key=True)
    version_id = models.ForeignKey(Version)  
    size = models.IntegerField(null=False)
    desc = models.CharField(max_length=1024, null=False)
    upload_time = models.DateTimeField(auto_now=True)
    download_url = models.URLField(null=False)

    def __str__(self):  
        return str(self.id)

class Release(models.Model):
    id = models.AutoField(primary_key=True)
    patch_id = models.ForeignKey(Patch)  
    serial_number = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    download_count = models.IntegerField(default=0)
    apply_count = models.IntegerField(default=0)
    is_enable = models.BooleanField(default=False)
    is_gray = models.BooleanField(default=False)
    pool_size = models.IntegerField(default=0)

    def __str__(self):  
        return str(self.id)

    def save(self, *args, **kw):
        if self.is_enable:
            releases = Release.objects.filter(patch_id=self.patch_id.id)
            releases.update(is_enable=False)
            result = releases.aggregate(number=Max('serial_number'))
            if result["number"] is None:
                self.serial_number = 1
            else:
                self.serial_number = result["number"] + 1
            self.is_enable = True
        super(Release, self).save(*args, **kw)
