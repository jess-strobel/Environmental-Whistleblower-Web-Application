from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Report, ReportForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

# Create your views here.
def index(request):
    return render(request, "whistleblowingapp/index.html")

def signedin(request):
    return render(request, "whistleblowingapp/signedin.html")

def logoutview(request):
    logout(request)
    return redirect("/whistleblowingapp")

def report(request):
    form = ReportForm()
    return render(request, "whistleblowingapp/submitreport.html", {"form" : form})

def allreports(request):
    data = Report.objects.all()
    context = {"reports": data}
    return render(request, "whistleblowingapp/allreports.html", context)


def submitreport(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            # Save the report using the form's cleaned data
            report = form.save(commit=False)  # Don't save to database yet

            if (request.user.is_authenticated):
                report.user = request.user
            else:
                report.user = None

            report.save()
            return HttpResponseRedirect(reverse("whistleblowingapp:submitted"))    
    else:
        form = ReportForm()
    return render(request, 'whistleblowingapp/submitted.html')
