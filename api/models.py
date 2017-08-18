from django.db import models
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _
import uuid
# Create your models here.


class DictObject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class System(DictObject):
    class Meta:
        verbose_name = "system"


class Category(DictObject):
    class Meta:
        verbose_name = "category"


class App(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category)
    system_id = models.ForeignKey(System)
    name = models.CharField(max_length=64, null=False, unique=True)
    key = models.CharField(max_length=1024, null=False, default=uuid.uuid4)
    secret = models.CharField(max_length=1024, null=False, default=uuid.uuid4)
    rsa = models.TextField(null=False)

    def __str__(self):
        return self.name


class Version(models.Model):
    id = models.AutoField(primary_key=True)
    app_id = models.ForeignKey(App)
    name = models.CharField(max_length=64, null=False, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Patch(models.Model):
    STATUS_WAIT = 0
    STATUS_ONLINE = 1
    STATUS_OFFLINE = 2

    STATUS_CHOICES = (
        (STATUS_WAIT, _('Wait')),
        (STATUS_ONLINE, _('Online')),
        (STATUS_OFFLINE, _('Offline')),
    )

    id = models.AutoField(primary_key=True)
    version_id = models.ForeignKey(Version)
    desc = models.CharField(max_length=1024, null=False)
    serial_number = models.IntegerField(default=1)
    download_url = models.URLField(null=False)
    size = models.IntegerField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    download_count = models.IntegerField(default=0)
    apply_count = models.IntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_WAIT)
    is_gray = models.BooleanField(default=False)
    pool_size = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kw):
        if self.status == self.STATUS_ONLINE:
            patchs = Patch.objects.all()
            patchs.update(status=self.STATUS_OFFLINE)
            result = patchs.aggregate(number=Max('serial_number'))
            if result["number"] is None:
                self.serial_number = 1
            else:
                self.serial_number = result["number"] + 1
            self.status = self.STATUS_ONLINE
        super(Patch, self).save(*args, **kw)
