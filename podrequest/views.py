from django.shortcuts import render
from podrequest.models import Device, RequestHistory
from django.views.generic import View, ListView, DetailView, UpdateView

#Authentication requirements
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

#Time utilities
import datetime
from django.utils.timezone import utc

# Create your views here.
def index(request):
    return render(request, 'podrequest/index.html')


class DeviceListView(ListView):
    model = Device
    template_name = 'podrequest/device_list.html'
    context_object_name = "device_list"


#This method uses the HTML name parameters to manipulate the model in the HTTP request
def requestdevice(request):
    if request.method == "POST":
        serialnumbers = getSerialNumbers(request)
        current_user = request.user

        if current_user.is_authenticated():
            # Do something for authenticated users.
            time_now = datetime.datetime.now().strftime('%H:%M:%S')  # Time like '23:12:05'
            date_now = datetime.datetime.now().strftime('%Y-%m-%d')  # Date like '2018/29/05'

            #Set the availablity of each serialnumber to False, that is, device is in use
            for serial in serialnumbers:
                Device.objects.filter(serialnumber=serial).update(available=False)
                RequestHistory.objects.create(date_requested=date_now,time_requested=time_now, serialnumber_id=serial, username_id=current_user.id)

        else:       
            # Do something for anonymous users.
            pass                   
      
    return HttpResponseRedirect(reverse('podrequest:requestdevice'))


class HistoryListView(ListView):
    model = RequestHistory
    template_name = 'podrequest/history.html'
    context_object_name = "request_history"


def returnDevice(request):
    if request.method == "POST":
        serialnumbers = getSerialNumbers(request)
        current_user = request.user

        if current_user.is_authenticated():
            # Do something for authenticated users.
            time_now = datetime.datetime.now().strftime('%H:%M:%S')  # Time like '23:12:05'
            date_now = datetime.datetime.now().strftime(
                '%Y-%m-%d')  # Date like '2018/29/05'

            #Set the availablity of each serialnumber to False, that is, device is in use
            for serial in serialnumbers:
                Device.objects.filter(serialnumber=serial).update(available=True)
                RequestHistory.objects.filter(date_requested=request.date_requested, time_requested=request.time_requested,
                                              serialnumber_id=serial, username_id=current_user.id).update(date_returned=date_now, time_returned=time_now)

        else:
            # Do something for anonymous users.
            pass
    
    return HttpResponseRedirect(reverse('podrequest:requesthistory'))


#Get the serialnumbers and csrf token from the POST request and return a list of serialnumbers
def getSerialNumbers(request_variable):
    #Store request items in a list
    pod_request_items = []
    for key, values in request_variable.POST.lists():
        pod_request_items += (key, values)

    #Serialnumbers are in the fourth position of the 'pod_request_items' list
    return pod_request_items[3]
