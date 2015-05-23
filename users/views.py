from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import View
from django.views.generic import TemplateView

from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import resolve, Resolver404
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
from users.models import Profile


class LoginPage(TemplateView):
    #template_name = 'users/login.html'
    def get(self, request):
        if(not request.user.is_authenticated()):
            redirectBool = False
            redirectDest = None
            if 'next' in request.GET:
                redirectBool = True
                redirectDest = request.GET['next']
            return render(request, 'users/login.html', {"user": request.user, "loggedin": request.user.is_authenticated(), "redirect": redirectBool, "redirectDest": redirectDest})
        else:
            return redirect('gallery')

    
    
class RegisterPage(TemplateView):
    #template_name = 'users/register.html'

    def get(self, request):
        if(not request.user.is_authenticated()):
            return render(request, 'users/register.html', {"user": request.user, "loggedin": request.user.is_authenticated()})
        else:
            return redirect('gallery')
    
    
class LogoutPage(View):
    """ Log the user out. """
    
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/gallery?logout=True')
        #return redirect('gallery')
        
        
class ProcessLog(View):
    """ Log the user in. """
    
    def post(self, request):
        
        #################
        # Get POST data #
        #################
        
        postData = request.POST
        
        try:
            username = postData['username']
            password = postData['password']
            
        except KeyError as e:
            response = "FAIL_POSTDATA::{}".format(e)
            return HttpResponseBadRequest(response)
            
            
        ##################
        # Authentication #
        ##################
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                if 'next' in postData:
                    try:

                        resolve(postData['next'])
                        return HttpResponseRedirect(postData['next'])
                    except Resolver404:
                        return redirect('gallery')
                
                # Everything is OK
                #return redirect('gallery')
                return redirect('gallery')
                
            else:
                # Account Disabled
                return HttpResponse('FAIL_ACC_DISABLED')
                
        else:
            # Authentication Failed
            return redirect('users_login')

# class ProcessReg(View):
#     def post(self, request):
#         form = UserCreationForm(request.POST)
#         if(form.is_valid()):
#             form.save()
#             return redirect('users_test')
#         else:
#             return HttpResponse(form)
            

class ProcessReg(View):
    """ Process the registration form. """
    
    class InvalidData(Exception):
        ''' The POST data that we received is bad in some way. '''
        pass
    
    def post(self, request):
        
        #################
        # Get POST data #
        #################
        
        postData = request.POST
        
        try:
            username = postData['username']
            firstName = postData['firstname']
            lastName = postData['lastname']
            email = postData['email']
            password = postData['password']
            
            gender = postData['gender']
            dresssize = int(postData['dresssize'])
            
        except KeyError as e:
            response = "FAIL_POSTDATA::{}".format(e)
            return HttpResponseBadRequest(response)
            
            
        ##############################
        # Serverside data validation #
        ##############################
        
        try:
            if '@' not in email or '.' not in email:
                raise self.InvalidData("Invalid Email")
                
            if gender not in (choice[0] for choice in Profile.GENDER_CHOICES):
                raise self.InvalidData("Invalid Gender")
                
            if User.objects.filter(username=username).exists():
                raise self.InvalidData("Username Taken")
                
            if User.objects.filter(email=email).exists():
                raise self.InvalidData("Email Taken")

            if dresssize > 100 or dresssize < 0:
                raise self.InvalidData(str(dresssize) + "Invalid Dress Size")
                
        except self.InvalidData as e:
            response = "FAIL_POSTDATA::{}".format(e)
            return HttpResponseBadRequest(response)
            
            
        #################
        # User creation #
        #################
        
        try:
            newUser = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=firstName,
                    last_name=lastName,
                )
                
        except Exception as e:
            response = "FAIL_USER::{}::{}".format(
                    str(e),
                    str(dict(postData)),
                )
            return HttpResponseBadRequest(response)
            
            
        ####################
        # Profile creation #
        ####################
        
        try:
            newProfile = Profile(user=newUser, gender=gender, dresssize=dresssize)
            newProfile.save()
            
        except Exception as e:
            response = "FAIL_PROFILE::{}::{}".format(
                    str(e),
                    str(dict(postData)),
                )
            return HttpResponseBadRequest(response)
            
            
        #######################
        # Log the new user in #
        #######################
        
        user = authenticate(username=username, password=password)
        login(request, user)
        
        
        ####################
        # Everything is OK #
        ####################
        
        #return redirect('users_test')
        return HttpResponse("user created")
   
        
class LoginTestView(View):
    """ Tests if the user is logged in. """
    
    #@method_decorator(login_required)
    def get(self, request):
        user = request.user
        
        if user.is_authenticated():
            return HttpResponse("USER '{}' LOGGED IN".format(user.username))
        else:
            return HttpResponse("NOT LOGGED IN")