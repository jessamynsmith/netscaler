# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView
from vips.forms import DeviceForm
from vips.models import Device


class IndexView(ListView):
    template_name = 'vips/index.html'
    model = Device
    context_object_name = 'devices'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['deviceform'] = DeviceForm()
        return context


class DeviceList(ListView):
    template_name = 'vips/device_list.html'
    context_object_name = 'devices'
    model = Device


class CreateDevice(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'vips/device_form.html'
    success_url = "/"
