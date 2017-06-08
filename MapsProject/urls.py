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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from apps.usermanage.views import HomePageView

urlpatterns = [
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.usermanage.urls'), name='usermanage'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^enterprise/', include('apps.enterprise.urls'), name='enterprise'),
    url(r'^client/', include('apps.client.urls'), name='client'),
    url(r'^service/', include('apps.service.urls'), name='service'),
    url('^route/', include('apps.route.urls'), name='route'),
    url('^help/', include('apps.help.urls'), name='help'),
    url('^event/', include('apps.event.urls'), name='event'),
    url('^notification/', include('apps.notification.urls'), name='notification'),
    url(r'^$', HomePageView.as_view(), name="index"),
)


