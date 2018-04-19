from django.conf.urls import url
from podrequest import views

#TEMPLATE URLS!
app_name = 'podrequest'

urlpatterns = [
    url(r'^$', views.DeviceListView.as_view(), name='device_list'),
    url(r'^requestDevice/', views.requestDevice, name='requestDevice'),
    url(r'^history/', views.HistoryListView.as_view(), name='requesthistory'),
    url(r'^returnDevice/', views.returnDevice, name='returnDevice'),
]
