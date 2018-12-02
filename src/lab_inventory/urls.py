"""lab_inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

#Since "views" is imported from two different apps
import auth_app
import podrequest


urlpatterns = [
    url(r'', include('auth_app.urls')),
    url(r'^podrequest/', include('podrequest.urls', namespace='podrequest')),
    url(r'^admin/', admin.site.urls),
    #Must specify which "views" is used to logout
    url(r'^logout/$', auth_app.views.user_logout, name='logout'),
    url(r'', include('password_reset.urls')),
]
