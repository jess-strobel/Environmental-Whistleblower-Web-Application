from django.shortcuts import render, redirect, get_object_or_404
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
    return render(request, "whistleblowingapp/signedin.html", {'posts': Report.objects.all()})

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

def viewreport(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.user.is_authenticated and request.user.is_staff and report.status == "New":
        # Update the status to "In Progress"
        report.status = "In Progress"
        report.save()


    if request.method == 'POST':
        # Process form submission
        report.status = request.POST.get('status')
        report.admin_notes = request.POST.get('admin_notes')
        report.save()
        return redirect('whistleblowingapp:signedin')
    
    return render(request, 'whistleblowingapp/viewreport.html', {'report':report})


def viewUserReports(request):
    data = Report.objects.filter(user=request.user)
    context = {"reports": data}
    return render(request, "whistleblowingapp/viewUserReports.html", context)