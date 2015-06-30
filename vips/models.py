from django.db import models

# Create your models here.

class Login(models.Model):
    user = models.CharField(max_length=16)
    password = models.CharField(max_length=16)

    def __unicode__(self):
        return '%s' % self.user


class Device(models.Model):
    ip = models.GenericIPAddressField()
    label = models.CharField(max_length=64)
    login = models.ForeignKey(Login)

    def __unicode__(self):
        return '%s' % self.label

class Vip(models.Model):
    name = models.CharField(max_length=64)
    state = models.CharField(max_length=16)
    address = models.GenericIPAddressField()
    device = models.ForeignKey(Device)

    def __unicode__(self):
        return '%s' % self.name
