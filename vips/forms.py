__author__ = 'dambl_000'

from django.forms import ModelForm, Form
from django import forms
from vips.models import Device

class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['label', 'ip', 'login']
