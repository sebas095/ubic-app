from django.shortcuts import render
from django.utils.decorators import method_decorator
from apps.service.models import Service
from django.contrib.auth.decorators import login_required

def require_service(view):
    def serviceOnly(function):
        def wrap(request, *args, **kwargs):
            if request.user.groups.all()[0].name == "superadmin" \
            or (request.user.groups.all()[0].name == "admin"
            and Service.objects.filter(enterprise__admin_by__username=request.user.username)
            and  Service.objects.filter(enterprise__admin_by__username=request.user.username)[0].is_active):
                return function(request, *args, **kwargs)
            return render(request, 'errors/service.html')
        return wrap

    view.dispatch = method_decorator(serviceOnly)(view.dispatch)
    return view

def require_login(view):
    def loginOnly(function):
        def wrap(request, *args, **kwargs):
            decorated_view_func = login_required(request)
            if not decorated_view_func.user.is_authenticated():
                return decorated_view_func(request)
            return function(request, *args, **kwargs)
        return wrap

    view.dispatch = method_decorator(loginOnly)(view.dispatch)
    return view
