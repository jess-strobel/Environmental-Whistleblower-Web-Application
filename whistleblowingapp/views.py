from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Report, ReportForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
import boto3
from django.conf import settings


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        logout(request)
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
        if (len(form.data.get('reportTitle')) > 255):
            form.add_error('reportTitle', 'Please ensure the title has less than 255 characters')
            return render(request, 'whistleblowingapp/submitreport.html', {'form': form})       
        if form.is_valid():
            # Validate file types
            jpeg = form.cleaned_data.get('reportJPEG')
            txt = form.cleaned_data.get('reportText')
            pdf = form.cleaned_data.get('reportPDF')

            if jpeg and jpeg.content_type != 'image/jpeg':
                form.add_error('reportJPEG', 'Only JPEG files are allowed.')
                return render(request, 'whistleblowingapp/submitreport.html', {'form': form})

            if txt and txt.content_type != 'text/plain':
                form.add_error('reportText', 'Only TXT files are allowed.')
                return render(request, 'whistleblowingapp/submitreport.html', {'form': form})

            if pdf and pdf.content_type != 'application/pdf':
                form.add_error('reportPDF', 'Only PDF files are allowed.')
                return render(request, 'whistleblowingapp/submitreport.html', {'form': form})

            # Save the report using the form's cleaned data
            report = form.save(commit=False)  # Don't save to database yet

            if request.user.is_authenticated:
                report.user = request.user
            else:
                report.user = None

            report.save()
            return render(request, 'whistleblowingapp/submitted.html')  
    else:
        form = ReportForm()
    return render(request, 'whistleblowingapp/submitreport.html', {'form': form})

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


def deleteReport(request, report_id):
    report = Report.objects.get(pk=report_id)

    if report.user != request.user and not request.user.is_superuser:
        raise PermissionDenied("You do not have permission to delete this report.")

    s3 = boto3.client('s3', 
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    if report.reportText:
        s3.delete_object(Bucket=bucket_name, Key=f'static/{report.reportText}')
    if report.reportPDF:
        s3.delete_object(Bucket=bucket_name, Key=f'static/{report.reportPDF}')
    if report.reportJPEG:
        s3.delete_object(Bucket=bucket_name, Key=f'static/{report.reportJPEG}')

    report.delete()

    return redirect('whistleblowingapp:viewUserReports')

def view_file(request, file_type, file_path):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    if file_type == 'txt':
        obj = s3.get_object(Bucket=bucket_name, Key=file_path)
        return HttpResponse(obj['Body'].read(), content_type='text/plain')
    elif file_type == 'jpeg':
        return HttpResponse(f'<img src="https://{bucket_name}.s3.amazonaws.com/{file_path}" />', content_type='text/html')
    elif file_type == 'pdf':
        return HttpResponse(f'<embed src="https://{bucket_name}.s3.amazonaws.com/{file_path}" width="100%" height="600px" />', content_type='text/html')
    else:
        return HttpResponse('Unsupported file type', status=400)

