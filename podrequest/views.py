from django.shortcuts import render
from podrequest.models import Device, RequestHistory
from django.views.generic import View, ListView, DetailView, UpdateView

#Time utilities
import datetime
from django.utils.timezone import utc

# Create your views here.
def index(request):
    return render(request, 'podrequest/index.html')


class DeviceListView(ListView):
    model = Device
    template_name = 'podrequest/index.html'
    context_object_name = "device_list"


#This method uses the HTML name parameters to manipulate the model in the HTTP request
def requestdevice(request):
    #Get the serialnumbers and csrf token from the POST request and store them in a list 
    pod_request_items = []
    for key, values in request.POST.lists():
        pod_request_items += (key, values)
        
        
    if request.method == "POST":
        current_user = request.user
        if current_user.is_authenticated():
            # Do something for authenticated users.
            time_now = datetime.datetime.now().strftime('%H:%M:%S')  # Time like '23:12:05'
            date_now = datetime.datetime.now().strftime('%Y/%m/%d')  # Date like '2018/29/05'

            #For every serialnumber in the list, set the availablity to False, that is, firewall is in use
            # The serialnumbers are in the fourth position of the 'pod_request_items' list
            for serial in pod_request_items[3]:
                Device.objects.filter(serialnumber=serial).update(available=False)
                #RequestHistory.update(date_requeted=date_now,time_requested=time_now, serialnumber=serial)

        else:       
            # Do something for anonymous users.
            pass                   
      
    return render(request, 'podrequest/device_list.html', {})




