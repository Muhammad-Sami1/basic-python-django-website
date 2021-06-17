from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.user.is_anonymous:
        messages.success(request, 'For contacting us you must login!')
        return redirect("/login")
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, "contact.html")


def loginUser(request): 
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/contact")
        else:
            return render(request, "login.html")
            messages.success(request, 'Please enter the right credentials or create a new account!')
    return render(request, "login.html")


def logoutUser(request):
    logout(request) 
    return redirect("/login")


def registerPage(request):
    form = UserCreationForm()
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Now you have to login to access contact us page!')
        else:
            messages.success(request, 'Account Not Created! Please enter the right credentials to create a new account! Your password must be of 8 characters and cannot be entirely numeric!')
    context =  {"form":form}
    return render(request, "register.html", context)
    
