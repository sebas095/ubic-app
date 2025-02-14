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
from .views import NotificationListAPI, NotificationCreateAPI, NotificationDeleteAPI, NotificationCountAPI

urlpatterns = [
    url(r'api/list/$', NotificationListAPI.as_view(), name='notification_list_api'),
    url(r'api/count/$', NotificationCountAPI.as_view(), name='notification_count_api'),
    url(r'api/create/$', NotificationCreateAPI.as_view(), name='notification_create_api'),
    url(r'api/delete/(?P<id>\w+)/$', NotificationDeleteAPI.as_view(), name='notification_delete_api')
]

