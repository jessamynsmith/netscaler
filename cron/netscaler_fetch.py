import os, sys

proj_path = "/Users/jeffrey.dambly/PycharmProjects/netscaler"
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

def main():
    """
    script to be run as a cron job. this gets all the devices and the fetchs all the information for each one
    :return:
    """

    devices = Device.objects.all()

    for device in devices:
        print "Fetching Vips from: %s" % device
        Vip.objects.vips_poll(device)
        for vip in device.vips.all():
            print "Fetching members from Device: %s Vip: %s" % (device, vip)
            try:
                Member.objects.members_poll(vip, debug=True)
            except TIMEOUT:
                print "TIMEOUT to device: %s" % device

if __name__ == "__main__":
    main()