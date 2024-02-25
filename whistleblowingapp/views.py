from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, "whistleblowingapp/index.html")

def signedin(request):
    return render(request, "whistleblowingapp/signedin.html")

def logoutview(request):
    logout(request)
    return redirect("/whistleblowingapp")