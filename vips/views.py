# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView
from vips.forms import DeviceForm
from vips.models import Device, Vip, Member


class IndexView(ListView):
    template_name = 'vips/index.html'
    model = Device
    context_object_name = 'devices'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['stategraph'] = Vip.objects.graph()
        return context


class AdminView(ListView):
    template_name = 'vips/deviceadmin.html'
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


class MemberView(ListView):
    template_name = 'vips/memberlist.html'
    model = Member
    context_object_name = 'members'

    def get_queryset(self):
        return self.model.objects.filter(vip__id=self.kwargs['pk'])
