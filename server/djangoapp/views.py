from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact_us.html', context)


# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username,password=password)

        if user is not None:
            print("valid user")
            login(request, user)
            # redirect
            return render(request,'djangoapp/index.html',context)
        else:
            print("invalid user")
            # redirect to login
            context = {"Error": "invalid password or username. Try Again"}
            return render(request,'djangoapp/index.html',context)
    else:
        context = {"Error": "Unsupported method"}
        return render(request,'djangoapp/index.html',context)


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    context = {}
    if request.user.is_authenticated is True:
        logout(request)
        return render(request,'djangoapp/index.html',context)
    else:
        context = {"Error": "Not logged in"}
        return render(request,"djangoapp/index.html",context)


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.user.is_authenticated is True:
        context = {"Error": "Already logged in"}
        return render(request,"djangoapp/index.html",context)
    if request.method == "GET":
        return render(request,'djangoapp/registration.html',context)
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm = request.POST["confirm"]
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]

        if len(username) == 0:
            context = {"Error": "Username cant be empty"}
            return render(request,'djangoapp/registration.html',context)
        
        if len(password) == 0:
            context = {"Error": "Password cant be empty"}
            return render(request,'djangoapp/registration.html',context)
        
        if len(confirm) == 0:
            context = {"Error": "Confirm password cant be empty"}
            return render(request,'djangoapp/registration.html',context)
        
        if len(first_name) == 0:
            context = {"Error": "First name cant be empty"}
            return render(request,'djangoapp/registration.html',context)
        
        if len(last_name) == 0:
            context = {"Error": "Last name cant be empty"}
            return render(request,'djangoapp/registration.html',context)

        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            user_exist = False

        if user_exist is True:
            context = {"Error": "Username already in use. Try Again"}
            return render(request,"djangoapp/registration.html",context)
        else:
            if password != confirm:
                context = {"Error": "Password and confirm password do not match"}
                return render(request,"djangoapp/registration.html",context)
            
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            login(request,user)
            return render(request,"djangoapp/index.html",context)
    else:
        context = {"Error": "Unsupported method"}
        return render(request,'djangoapp/registration.html',context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        #url = "https://albertoceba1-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        url = "http://localhost:3000/dealerships/get"
        data = get_dealers_from_cf(url)
        context = {"dealerships": data}
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request,dealer_id):
    context = {}
    if request.method == "GET":
        return render(request,'djangoapp/dealer_details.html',context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request,dealer_id):
    pass

