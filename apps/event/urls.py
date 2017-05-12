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

from .views import EventCreateView, EventUpdateView, EventListView, EventDeleteView, \
                LoanCreateView, LoanUpdateView, LoanListView, LoanDeleteView, \
                EventAPIView, EventCreateAPIView

urlpatterns = [
    url(r'api/new/$', EventCreateAPIView.as_view(), name='event_create_new_api'),
    url(r'api/create/$', EventAPIView.as_view(), name='event_create_api'),
    url(r'loan/create/$', LoanCreateView.as_view(), name='loan_create'),
    url(r'loan/edit/(?P<id>\w+)/$', LoanUpdateView.as_view(), name='loan_edit'),
    url(r'loan/list/$', LoanListView.as_view(), name='loan_list'),
    url(r'loan/delete/(?P<id>\w+)/$', LoanDeleteView.as_view(), name='loan_delete'),
    url(r'create/$', EventCreateView.as_view(), name='event_create'),
    url(r'edit/(?P<id>\w+)/$', EventUpdateView.as_view(), name='event_edit'),
    url(r'list/$', EventListView.as_view(), name='event_list'),
    url(r'delete/(?P<id>\w+)/$', EventDeleteView.as_view(), name='event_delete'),
]

