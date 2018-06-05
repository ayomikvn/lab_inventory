from django.conf.urls import url
from podrequest import views
from django.contrib.auth.decorators import login_required

#TEMPLATE URLS!
app_name = 'podrequest'

urlpatterns = [
    url(r'^$', login_required(views.DeviceListView.as_view()), name='device_list'),
    url(r'^requestDevice/', views.request_device, name='request_device'),
    url(r'^history/', login_required(views.HistoryListView.as_view()), name='requesthistory'),
    url(r'^returnDevice/', views.return_device, name='return_device'),
    url(r'^(?P<pk>[-\w]+)/$', login_required(views.DeviceDetailView.as_view()),
        name='device_detail'),
]
