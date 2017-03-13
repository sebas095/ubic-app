from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from apps.service.models import Service

def require_service(view):
    def serviceOnly(function):
        def wrap(request, *args, **kwargs):
            if request.user.groups.all()[0].name == "superadmin" \
            or (request.user.groups.all()[0].name == "admin"
            and Service.objects.filter(enterprise__admin_by__username=request.user.username)
            and  Service.objects.filter(enterprise__admin_by__username=request.user.username)[0].is_active):
                return function(request, *args, **kwargs)
            return HttpResponseForbidden()
        return wrap

    view.dispatch = method_decorator(serviceOnly)(view.dispatch)
    return view