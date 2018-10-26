from django.contrib.auth import get_user_model
from django.shortcuts import render
from podrequest.models import Device, RequestHistory
from django.views.generic import View, ListView, DetailView, UpdateView

#Use this to return Json instead of HTTP response
from django.http import JsonResponse

#Authentication requirements
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#Time utilities
import datetime
from django.utils.timezone import utc


from django.contrib import messages


"""
    ========================================
    Class Based Views for Device and History
    ========================================
"""
#Display the devices (and users using them if applicable) as a list in the browser
class DeviceListView(ListView):
    model = Device
    template_name = 'podrequest/device_list.html'
    paginate_by =15
    #Order result set by Podnumber in ascending order
    queryset = Device.objects.order_by('podnumber')

    def get_context_data(self, **kwargs):
        context = super(DeviceListView, self).get_context_data(**kwargs)
    
        #Get the usernames (firstname and lastname) and serialnumbers from database, where the device is in use
        history_detail_ids = RequestHistory.objects.filter(date_returned=None).values('username_id','serialnumber_id')

        #List of Dictionaries storing serialnumbers and usernames (firstname and lastname)
        list_of_details=[]
        #Variable used to insert a new serialnumber-value pair for each dictionary in the list above
        position = 0

        for user in history_detail_ids:
            list_of_details += get_user_model().objects.filter(id=user['username_id']).values('first_name','last_name')
            list_of_details[position]['serialnumber_id'] = user['serialnumber_id']
            position += 1
        
        context['users_using_pod'] = list_of_details

        return context


class DeviceDetailView(DetailView):
    model = Device
    template = 'podrequest/device_detail.html'
    context_object_name = 'device_detail'

    def get_context_data(self, **kwargs):
        context = super(DeviceDetailView, self).get_context_data(**kwargs)

        #Get devices that have not been returned from the RequestHistory table
        history_details_query_set = RequestHistory.objects.filter(date_returned=None).values('id','serialnumber_id')
        #List to store each row of data from the above queryset
        history_details=[]
        #for each itme in the query set, add it to the previous list
        for history in history_details_query_set:
            history_details.append(history)

        #Inject history_details into the View    
        context['history_details'] = history_details
    
        return context        


class HistoryListView(ListView):
    model = RequestHistory
    template_name = 'podrequest/history.html'
    paginate_by =40
    #Order result set by date_requested, then time_requested, in descending order
    queryset = RequestHistory.objects.order_by('-id')


    def get_context_data(self, **kwargs):
        context = super(HistoryListView, self).get_context_data(**kwargs)

        #Get the usernames and serialnumbers from database, where the device is in use
        #Distinct is used because we don't need more than one instance of the values to filter in the 'for' loop in the history page
        history_detail_ids = RequestHistory.objects.distinct().values(
            'username_id', 'serialnumber_id')

        #List of Dictionaries storing serialnumbers and usernames (firstname and lastname)
        list_of_details = []
        position = 0

        for pod in history_detail_ids:
            list_of_details += Device.objects.filter(
                serialnumber=pod['serialnumber_id']).values('podnumber', 'device_model', 'serialnumber')
            list_of_details[position]['user_id'] = pod['username_id']
            position += 1

        context['pod_details'] = list_of_details

        return context



"""
    =================================================
    Custom Views for requesting and returning Devices
    =================================================
"""

#This method uses the HTML name parameters to manipulate the model in the HTTP request
def request_device(request):

    if request.method == "POST":
        try:
            serialnumber_list = get_primary_key_list(request)
        except:
            messages.error(
                request, 'You did not select any Pods.')
            return HttpResponseRedirect(request.path)

        current_user = request.user

        if current_user.is_authenticated:
            # Do something for authenticated users.
            time_now = datetime.datetime.now().strftime('%H:%M:%S')  # Time like '23:12:05'
            date_now = datetime.datetime.now().strftime('%Y-%m-%d')  # Date like '2018/29/05'
            
            #Set the availablity of each serialnumber to False, that is, device is in use
            for serialnumber in serialnumber_list:
                if is_device_available(serialnumber):
                    Device.objects.filter(
                        serialnumber=serialnumber).update(available=False)
                    RequestHistory.objects.create(
                        date_requested=date_now, time_requested=time_now, serialnumber_id=serialnumber, username_id=current_user.id)

                else:
                    messages.error(request, 'One or more of the Pods you requested is already in use.')
                    return HttpResponseRedirect(request.path)

            messages.success(
                request, 'Pod request successful.')
            return HttpResponseRedirect(request.path)

        else:       
            # Do something for anonymous users.
            return HttpResponse("You're not logged in! Please login to continue.")
      
    return HttpResponseRedirect(reverse('podrequest:device_list'))


#This method updates the availablity of a firewall in Device table and the datetime in the RequestHistory table
def return_device(request):
    if request.method == "POST":
        try:
            request_history_id_list = []
            request_history_id_list = get_primary_key_list(request)
        except:
            messages.error(
                request, 'You did not select any Pods.')
            return HttpResponseRedirect(request.path)

        current_user = request.user

        if current_user.is_authenticated:
            # Do something for authenticated users.
            time_now = datetime.datetime.now().strftime('%H:%M:%S')  # Time like '23:12:05'
            date_now = datetime.datetime.now().strftime(
                '%Y-%m-%d')  # Date like '2018/29/05'

            #Set the availablity of each serialnumber to False, that is, device is in use
            for request_history_id in request_history_id_list:
                RequestHistory.objects.filter(id=request_history_id).update(date_returned=date_now, time_returned=time_now)
                serialnum = RequestHistory.objects.filter(id=request_history_id).values('serialnumber_id')  # Get the serialnumber queryset as a list from History table
                serialnum=serialnum[0]['serialnumber_id'] #Retrieve the serialnumber from position 0 of array and call it as a key-value pair
                Device.objects.filter(serialnumber=serialnum).update(available=True) #Make device available by setting Device.available to True
                

            messages.success(
                    request, 'Returned Pod(s) successfully.')
            return HttpResponseRedirect(request.path)

        else:
            # Do something for anonymous users.
            return HttpResponse("You're not logged in! Please login to continue.")
    
    return HttpResponseRedirect(reverse('podrequest:requesthistory'))





"""
================================================================
Custom Methods
================================================================
"""
#Get the model primary key (e.g. serialnumber, request history_id) and csrf token from the POST request and return a list of primary keys
def get_primary_key_list(web_request):
    #Store request items in a list
    requested_items = []
    for key, values in web_request.POST.lists():
        requested_items += (key, values)

    #Serialnumbers are in the fourth position of the 'pod_request_items' list
    return requested_items[3]


#Checks to see if a Device is available
def is_device_available(serial):
    get_query = Device.objects.filter(serialnumber=serial).values('available')
    return get_query[0]['available']

