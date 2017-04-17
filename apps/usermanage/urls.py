from django.conf.urls import url

from .views import HomePageView, RegView, UserListView, UserUpdateView, DeactivateAccountView

urlpatterns = [
    url(r'accounts/register/$', RegView.as_view(), name="regular_reg"),
    url(r'user/list/$', UserListView.as_view(), name="userlist"),
    url(r'user/edit/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user_edit'),
    url(r'user/deactivate/(?P<pk>\d+)/$', DeactivateAccountView.as_view(), name='user_deactivate'),
]