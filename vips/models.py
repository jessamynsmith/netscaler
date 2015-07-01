from django.db import models

# Create your models here.
from vips.fetch import Netscaler


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

class VipManager(models.Manager):

    def poll(self, device=Device):
        """
        takes a query object of type Device, connects to that host, and then gets
        all the vip info

        then all the information is entered into the database
        :param device: query object
        :return:
        """

        remote = Netscaler(host=device.ip,
                           username=device.login.user,
                           password=device.login.password)

        for vipkey, vipval in remote.get_vips().iteritems():
            Vip.objects.update_or_create(name=vipval['Name'],
                                         address=vipval['IPAddress'],
                                         state=vipval['State'],
                                         device=device)


class Vip(models.Model):
    name = models.CharField(max_length=64)
    state = models.CharField(max_length=16)
    address = models.GenericIPAddressField()
    device = models.ForeignKey(Device)
    updated = models.DateTimeField(auto_now=True)

    objects = VipManager()

    def __unicode__(self):
        return '%s' % self.name
