# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from vips.forms import DeviceForm
from vips.models import Device


class AdminView(ListView):
    template_name = 'vips/index.html'
    model = Device
    context_object_name = 'devices'

    def get_context_data(self, **kwargs):
        context = super(AdminView, self).get_context_data(**kwargs)
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


class DeleteDevice(DeleteView):
    model = Device
    template_name = 'vips/deleteform.html'
    success_url = "/"