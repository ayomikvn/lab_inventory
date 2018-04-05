from django.shortcuts import render
from podrequest.models import Device
from django.views.generic import View,ListView

# Create your views here.
def index(request):
    return render(request, 'podrequest/index.html')


class DeviceListView(ListView):
    model = Device
    template_name = 'podrequest/index.html'
    context_object_name = "device_list"
