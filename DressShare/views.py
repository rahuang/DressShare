import sys

from django.core.exceptions import PermissionDenied
from django.http import (HttpResponse, HttpResponseNotFound,
    HttpResponseBadRequest, HttpResponseServerError)
from django.views.generic.base import View
from django.views.generic import TemplateView

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from store.models import *
from users.models import *

class ErrorView(View):
    """ HTTP 500: Internal Server Error """
    template_name = '500.html'
    status = 500
    
    def get(self, request):
        return render(request, self.template_name, status=self.status)
    
    
class PermissionDeniedView(ErrorView):
    """ HTTP 403: Forbidden """
    template_name = '403.html'
    status = 403
    
    
class NotFoundView(ErrorView):
    """ HTTP 404: Not Found """
    template_name = '404.html'
    status = 404
    
    
class IndexPage(TemplateView):
    """ The Index Page. """
    #template_name = 'index.html'

    def get(self, request):
        return render(request, "index.html", {"user": request.user, "loggedin": request.user.is_authenticated()})

class Gallery(TemplateView):

    #@method_decorator(login_required)
    def get(self, request):
        user = request.user
        #profileUser = Profile.objects.filter(user=user)
        logout = False
        if 'logout' in request.GET and request.GET['logout'] == "True":
            logout = True

        dresses = Dress.objects.filter(availability=True)
        return render(request, "gallery.html", {"dresses": dresses, "user": request.user, "loggedin": request.user.is_authenticated(), "logout": logout})

class Details(TemplateView):
    #@method_decorator(login_required)
    def get(self, request, id_name=None):
        if(id_name == None):
            return redirect('gallery')

        try:
            id_name = int(id_name)
        except:
            return redirect('gallery')

        try:
            dress = Dress.objects.get(id=id_name)
        except:
            return HttpResponse("Invalid Dress")
        
        return render(request, "details.html", {"dress": dress, "user": request.user, "loggedin": request.user.is_authenticated()})
    
    
def staff_only(view):
    """ Staff-only View decorator. """
    
    def decorated_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
            
        if not request.user.is_staff:
            raise PermissionDenied
            
        return view(request, *args, **kwargs)
        
    return decorated_view
    
    