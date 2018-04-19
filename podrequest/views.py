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



#Get the model primary key (e.g. serialnumber, request history_id) and csrf token from the POST request and return a list of primary keys
def getModelPrimaryKeyList(request_variable):
    #Store request items in a list
    requested_items = []
    for key, values in request_variable.POST.lists():
        requested_items += (key, values)

    #Serialnumbers are in the fourth position of the 'pod_request_items' list
    return requested_items[3]



#Display the devices as a list pulled from Device table
class DeviceListView(ListView):
    model = Device
    template_name = 'podrequest/device_list.html'
    context_object_name = "device_list"
    #paginate_by =10



#This method uses the HTML name parameters to manipulate the model in the HTTP request
def requestDevice(request):
    if request.method == "POST":
        serialnumber_list = getModelPrimaryKeyList(request)
        current_user = request.user

        if current_user.is_authenticated():
            # Do something for authenticated users.
            time_now = datetime.datetime.now().strftime('%H:%M:%S')  # Time like '23:12:05'
            date_now = datetime.datetime.now().strftime('%Y-%m-%d')  # Date like '2018/29/05'

            #Set the availablity of each serialnumber to False, that is, device is in use
            for serialnumber in serialnumber_list:
                Device.objects.filter(serialnumber=serialnumber).update(available=False)
                RequestHistory.objects.create(date_requested=date_now,time_requested=time_now, serialnumber_id=serialnumber, username_id=current_user.id)

        else:       
            # Do something for anonymous users.
            print("You're not logged in! Please login to continue.")
      
    return HttpResponseRedirect(reverse('podrequest:device_list'))


class HistoryListView(ListView):
    model = RequestHistory
    template_name = 'podrequest/history.html'
    context_object_name = "request_history"



#This method updates the availablity of a firewall in Device table and the datetime in the RequestHistory table
def returnDevice(request):
    if request.method == "POST":
        request_history_id_list = getModelPrimaryKeyList(request)
        current_user = request.user

        if current_user.is_authenticated():
            # Do something for authenticated users.
            time_now = datetime.datetime.now().strftime('%H:%M:%S')  # Time like '23:12:05'
            date_now = datetime.datetime.now().strftime(
                '%Y-%m-%d')  # Date like '2018/29/05'
   
            #Set the availablity of each serialnumber to False, that is, device is in use
            for request_history_id in request_history_id_list:
                RequestHistory.objects.filter(id=request_history_id).update(
                    date_returned=date_now, time_returned=time_now)
                serialnum = RequestHistory.objects.filter(id=request_history_id).values(
                    'serialnumber_id')  # Get the serialnumber from History table
                Device.objects.filter(serialnumber=serialnum).update(available=True) #Make device available by setting Device.available to True
    
        else:
            # Do something for anonymous users.
            print("You're not logged in! Please login to continue.")
    
    return HttpResponseRedirect(reverse('podrequest:requesthistory'))
