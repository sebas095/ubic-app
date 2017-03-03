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
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from usermanage.views import HomePageView, RegView, UserListView, UserUpdateView, DeactivateAccountView
from enterprise.views import EnterpriseCreateView

urlpatterns = [

]
urlpatterns += i18n_patterns(
    url(r'^accounts/register/$', RegView.as_view(), name="regular_reg"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/list/$', UserListView.as_view(), name="userlist"),
    url(r'^user/edit/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user_edit'),
    url(r'^user/deactivate/(?P<pk>\d+)/$', DeactivateAccountView.as_view(), name='user_deactivate'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', HomePageView.as_view(), name="index"),
    url(r'^enterprise/create', EnterpriseCreateView.as_view(), name='enterpise_create'),
)