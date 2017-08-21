from django.db import models
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _
import uuid
import sys
# Create your models here.


class DictObject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class System(DictObject):
    pass


class Category(DictObject):
    pass


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
    STATUS_DELETED = 0
    STATUS_WAITING = 1
    STATUS_RELEASED = 2
    STATUS_PRERELEASED = 3
    STATUS_STOPED = 4

    STATUS_CHOICES = (
        (STATUS_WAITING, _('Waiting')),
        (STATUS_RELEASED, _('Released')),
        (STATUS_STOPED, _('Stoped')),
        (STATUS_PRERELEASED, _('PreReleased')),
        (STATUS_DELETED, _('Deleted')),
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
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_WAITING)
    pool_size = models.BigIntegerField(default=sys.maxsize)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kw):
        status = self.status
        if self.status in (self.STATUS_RELEASED, self.STATUS_PRERELEASED):
            patchs = Patch.objects.all()
            patchs.filter(status__gt=self.STATUS_WAITING).update(status=self.STATUS_STOPED)
            result = patchs.aggregate(number=Max('serial_number'))
            if result["number"] is None:
                self.serial_number = 1
            else:
                self.serial_number = result["number"] + 1
            self.status = status
        super(Patch, self).save(*args, **kw)
    def supersave(self, *args, **kw):
        super(Patch, self).save(*args, **kw)
