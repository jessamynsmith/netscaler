# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView
from vips.models import Device


class IndexView(TemplateView):
    template_name = 'vips/index.html'


class DeviceList(ListView):
    template_name = 'vips/device_list.html'
    context_object_name = 'devices'
    model = Device


class CreateDevice(CreateView):
    model = Device
    template_name = 'vips/device_form.html'
    fields = ['label', 'ip', 'login']
    success_url = "/"
