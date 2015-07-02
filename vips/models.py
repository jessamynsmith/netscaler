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

class ServerManager(models.Manager):

    def server_poll(self, device=Device):
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

        for key, val in remote.get_servers().iteritems():
            Server.objects.update_or_create(name=val['Name'],
                                         address=val['IPAddress'],
                                         state=val['State'],
                                         device=device)


class Server(models.Model):
    name = models.CharField(max_length=64)
    state = models.CharField(max_length=16)
    address = models.GenericIPAddressField()
    device = models.ForeignKey(Device, related_name='servers')
    updated = models.DateTimeField(auto_now=True)

    objects = ServerManager()

    def __unicode__(self):
        return '%s' % self.name

class Vip(models.Manager):
    label = models.CharField(max_length=32)
    address = models.GenericIPAddressField()
    port = models.IntegerField()
    state = models.CharField(max_length=16)
    effective_state = models.CharField(max_length=16)
    device = models.ForeignKey(Device, related_name='vips')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s' % self.label
