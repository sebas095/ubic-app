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
from rest_framework_jwt.views import obtain_jwt_token
from .views import RoutePageView, RouteUpdateView, RouteDeleteView, \
                   RouteListView, RouteAPI, RouteListAPI

urlpatterns = [
    url(r'api/token-auth/$', obtain_jwt_token),
    url(r'api/list/$', RouteListAPI.as_view(), name='route_list_api'),
    url(r'api/(?P<id>\w+)/$', RouteAPI.as_view(), name='route_api'),
    url(r'create/$', RoutePageView.as_view(), name='route_create'),
    url(r'edit/(?P<id>\w+)/$', RouteUpdateView.as_view(), name='route_edit'),
    url(r'delete/(?P<id>\w+)/$', RouteDeleteView.as_view(), name='route_delete'),
    url(r'list/$', RouteListView.as_view(), name='route_list'),
]

