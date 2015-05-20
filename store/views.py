import sys

from django.core.exceptions import PermissionDenied
from django.http import (HttpResponse, HttpResponseNotFound,
    HttpResponseBadRequest, HttpResponseServerError)
from django.views.generic.base import View
from django.views.generic import TemplateView

from django.shortcuts import render

from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from store.models import *
from users.models import *


class TestPage(TemplateView):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        #print user
        profileUser = Profile.objects.filter(user=user)
        dresses = Dress.objects.filter(owner=profileUser)
        #return HttpResponse(profileUser)
        
        if user.is_authenticated():
            return render(request, "test1.html", {"username": user.username, "dresses": dresses})

# class AddDress(TemplateView):
#     @method_decorator(login_required)
#     def get(self, request):
#         user = request.user
#         print user
#         profileUser = Profile.objects.filter(user=user)
#         dresses = Dress.objects.filter(owner=profileUser)
#         return HttpResponse(profileUser)
        
#         if user.is_authenticated():
#             return render(request, "test1.html", {"username": user.username, "dresses": dresses})


class AddDress(TemplateView):
    #template_name = 'users/register.html'
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'add-dress.html')

class ProcessDress(TemplateView):
    #template_name = 'users/register.html'

    class InvalidData(Exception):
        ''' The POST data that we received is bad in some way. '''
        pass


    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        profileUser = Profile.objects.get(user=user)
        postData = request.POST
        postFiles = request.FILES

        try:
            name = postData['name']
            thumbnail = request.FILES['thumbnail']
        except KeyError as e:
            response = "FAIL_POSTDATA::{}".format(e)
            return HttpResponseBadRequest(response)

        try:
            newDress = Dress(name=name, owner=profileUser, thumbnail=thumbnail)
            newDress.save()
            
        except Exception as e:
            response = "FAIL_DRESS::{}::{}".format(
                    str(e),
                    str(dict(postData)),
                )
            return HttpResponseBadRequest(response)


        return HttpResponse("added dress <a href='/store/test1'>click here</a>")