from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth import authenticate, login, logout

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="password")
    
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
       return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/user.html")
   
def login_request(request):
    if request.user.is_authenticated:
       return HttpResponseRedirect(reverse("users:index"))
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = form.data["username"]
        password = form.data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html",{
                "message": "Invalid credentials,pls enter new ones",
                "form": LoginForm,
            })
    return render(request,"users/login.html",{
        "form": LoginForm,
    })
    
def logout_view(request):
    logout(request)
    return render(request, "users/login.html",{
        "message": "Logged out.",
        "form": LoginForm,
    })