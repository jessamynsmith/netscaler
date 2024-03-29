from django.db import models

# Create your models here.
from django.db.models import Count
from vips.fetch import Netscaler


class Login(models.Model):
    user = models.CharField(max_length=16)
    password = models.CharField(max_length=16)

    def __unicode__(self):
        return '%s %s' % (self.user, self.password)


class Device(models.Model):
    ip = models.GenericIPAddressField()
    label = models.CharField(max_length=64)
    login = models.ForeignKey(Login)

    class Meta:
        ordering = ('label',)

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


class VipManager(models.Manager):

    def vips_poll(self, device=Device, debug=False):
        """
        connects to the netscaler gets all the vip data and enters it into the db
        :return:
        """
        remote = Netscaler(host=device.ip,
                           username=device.login.user,
                           password=device.login.password)

        for key, val in remote.get_vips(debug=debug).iteritems():
            Vip.objects.update_or_create(label=val['label'],
                                         address=val['address'],
                                         port=val['port'],
                                         state=val['state'],
                                         effective_state=val['effective state'],
                                         device=device)

    def graph(self):
        colors =["#f30000",
                 "#0600f3",
                 "#00b109",
                 "#14e4b4",
                 "#0fe7fb",
                 "#67f200",
                 "#ff7e00",
                 "#8fe4fa",
                 "#ff5300",
                 "#640000",
                 "#3854d1",
         ]
        result = Vip.objects.values('state').annotate(value=Count('state'))

        i = 1
        for each in result:
            try:
                each.update({'color': colors[i]})
            except IndexError:
                i = 1
            i += 1
            if i > len(colors):
                i = 1

        return result

    def vips_per_device_graph(self):
        colors =["#f30000",
                 "#0600f3",
                 "#00b109",
                 "#14e4b4",
                 "#0fe7fb",
                 "#67f200",
                 "#ff7e00",
                 "#8fe4fa",
                 "#ff5300",
                 "#640000",
                 "#3854d1",
         ]

        result = Vip.objects.values('device__label').annotate(value=Count('label'))

        #todo there must be a better way to do this....
        i = 1
        for each in result:
            try:
                each.update({'color': colors[i]})
            except IndexError:
                i = 1
            i += 1
            if i > len(colors):
                i = 1

        return result

class Vip(models.Model):
    label = models.CharField(max_length=32)
    address = models.GenericIPAddressField()
    port = models.IntegerField()
    state = models.CharField(max_length=16)
    effective_state = models.CharField(max_length=16)
    device = models.ForeignKey(Device, related_name='vips', default=None, null=True)
    updated = models.DateTimeField(auto_now=True)

    objects = VipManager()

    def __unicode__(self):
        return '%s' % self.label


class MemberManager(models.Manager):

    def members_poll(self, vip=Vip, debug=False):
        """

        :param device:
        :return:
        """
        remote = Netscaler(host=vip.device.ip,
                           username=vip.device.login.user,
                           password=vip.device.login.password)

        for key, val in remote.get_members(vip.label).iteritems():
            if debug == True:
                print key, val
            if val != 'empty':
                Member.objects.update_or_create(label=val['label'],
                                                address=val['address'],
                                                port=val['port'],
                                                protocol=val['protocol'],
                                                state=val['state'],
                                                vip=vip)


class Member(models.Model):
    label = models.CharField(max_length=32)
    address = models.GenericIPAddressField()
    port = models.IntegerField()
    protocol = models.CharField(max_length=16)
    state = models.CharField(max_length=16)
    vip = models.ForeignKey(Vip, related_name='members')
    update = models.DateTimeField(auto_now=True)

    objects = MemberManager()

    def __unicode__(self):
        return '%s' % self.label
