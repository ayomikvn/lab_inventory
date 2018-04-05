from django.conf.urls import url
from podrequest import views

#TEMPLATE URLS!
app_name = 'podrequest'

urlpatterns = [
    url(r'^$', views.DeviceListView.as_view(), name='index'),
]
