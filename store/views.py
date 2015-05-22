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


class TestPage(TemplateView):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        #print user
        #profileUser = Profile.objects.filter(user=user)
        dresses = Dress.objects.filter(owner=user)
        #return HttpResponse(profileUser)
        
        if user.is_authenticated():
            return render(request, "test1.html", {"username": user.username, "dresses": dresses, "user": request.user, "loggedin": request.user.is_authenticated()})

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
        return render(request, 'add-dress.html', {"user": request.user, "loggedin": request.user.is_authenticated()})

class ProcessDress(TemplateView):
    #template_name = 'users/register.html'

    class InvalidData(Exception):
        ''' The POST data that we received is bad in some way. '''
        pass


    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        #profileUser = Profile.objects.get(user=user)
        postData = request.POST
        postFiles = request.FILES
        picture = None

        try:
            name = postData['name']
            if 'picture' in postFiles:
                picture = request.FILES['picture']
            color = postData['color'].lower()
            descript = postData['description']
            size = int(postData['size'])
            length = postData['length']
            formality = postData['formality']
        except KeyError as e:
            response = "FAIL_POSTDATA::{}".format(e)
            return HttpResponseBadRequest(response)


        try:
            if length not in (l[0] for l in Dress.LENGTH_CHOICES):
                raise self.InvalidData("Invalid Length")

            if formality not in (f[0] for f in Dress.FORMALITY_CHOICES):
                raise self.InvalidData("Invalid Formality")

            if size > 100 or size < 0:
                raise self.InvalidData(str(dresssize) + "Invalid Dress Size")
                
        except self.InvalidData as e:
            response = "FAIL_POSTDATA::{}".format(e)
            return HttpResponseBadRequest(response)


        try:
            newDress = Dress(name=name, owner=user, picture=picture, description=descript, color=color, size=size, length=length, formality=formality, availability=True)
            newDress.save()
        except Exception as e:
            response = "FAIL_DRESS::{}::{}".format(
                    str(e),
                    str(dict(postData)),
                )
            return HttpResponseBadRequest(response)


        return HttpResponse("added dress <a href='/store/test1'>click here</a>")


class ProcessFit(TemplateView):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        getData = request.GET

        try:
            dressID = int(getData['id'])
        except:
            return redirect('gallery')

        try:
            dress = Dress.objects.get(id=dressID)
            if not FittingRoom.objects.filter(user=user, dress=dress).exists():
                newFittingRoom = FittingRoom(user=user, dress=dress)
                newFittingRoom.save()
        except:
            return HttpResponse("Invalid Dress")

        return redirect('fitting-room')

    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        postData = request.POST

        if 'remove' in postData:
            remove = postData.getlist('remove')
            for fit in remove:
                try:
                    FittingRoom.objects.get(id=fit).delete()
                except:
                    pass

        return redirect('fitting-room')


class FittingRoomView(TemplateView):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        edit = False

        if 'edit' in request.GET:
            if request.GET['edit'] == "True":
                edit = True

        try:
            fitroom = FittingRoom.objects.filter(user=user)
        except:
            return HttpResponse("Invalid Dress")

        return render(request, 'fitting-room.html', {"user": request.user, "loggedin": request.user.is_authenticated(), "fitroom": fitroom, "edit": edit}) 
