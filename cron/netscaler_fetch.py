import argparse
import os, sys
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import traceback

proj_path = "/home/CORP/jeffrey.dambly/netscaler"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netscaler.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from vips.models import Device, Vip, Member
from pexpect import TIMEOUT

def updateAll():
    """
    script to be run as a cron job. this gets all the devices and the fetchs all the information for each one
    :return:
    """

    devices = Device.objects.all()

    for device in devices:
        print "Fetching Vips from: %s" % device
        try:
            Vip.objects.vips_poll(device)
        except TIMEOUT:
            print "TIMEOUT to device: %s" % device
        for vip in device.vips.all():
            print "Fetching members from Device: %s Vip: %s" % (device, vip)
            try:
                Member.objects.members_poll(vip, debug=True)
            except TIMEOUT:
                print "TIMEOUT to device: %s" % device

def updateDevice(name='', debug=False):

    try:
        device = Device.objects.get(Q(label=name) | Q(ip=name))
    except ObjectDoesNotExist:
        print 'Device with name: %s NOT FOUND' % name
        return False

    print 'Fetching Vips from: %s' % device
    try:
        Vip.objects.vips_poll(device, debug=debug)
    except TIMEOUT:
        print 'Timeout connecting to this device'
        if debug == True:
            traceback.print_exc()
        return False

    for vip in device.vips.all():
        print "Fetching members from Device: %s Vip: %s" % (device, vip)
        try:
            Member.objects.members_poll(vip, debug=debug)
        except TIMEOUT:
            if debug == True:
                traceback.print_exc()

            print "TIMEOUT to device: %s" % device

def main():

    parser = argparse.ArgumentParser(description='Script to poll and update Netscaler vips/members')
    parser.add_argument('-n', '--name', help='device hostname or ipaddress', dest='name')
    parser.add_argument('-d', '--debug', action='store_true', help='enables debuging output')

    args = parser.parse_args()

    if args.name:
        updateDevice(name=args.name, debug=args.debug)
    else:
        updateAll()


if __name__ == "__main__":
    main()