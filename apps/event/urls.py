"""MapsProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url

from .views import EventCreateView, EventUpdateView, EventListView

urlpatterns = [
    url(r'create', EventCreateView.as_view(), name='event_create'),
    url(r'edit/(?P<pk>\d+)/$', EventUpdateView.as_view(), name='event_edit'),
    url(r'list/$', EventListView.as_view(), name='event_list'),
    #url(r'deactivate/(?P<pk>\d+)/$', ClientDeactivateView.as_view(), name='event_deactivate'),
]

