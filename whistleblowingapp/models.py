from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    admin = models.BooleanField()
    user = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    def __str__(self):
        return self.user
    def isadmin(self):
        return self.admin == True
    
class Report(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    reportTitle = models.CharField(max_length=255, default='')
    reportDescription = models.TextField(default='')
    reportText = models.FileField(upload_to='report_txt/', blank=True, null=True)
    reportPDF = models.FileField(upload_to='report_pdf/', blank=True, null=True)
    reportJPEG = models.ImageField(upload_to='report_image/', blank=True, null=True)
    status = models.CharField(max_length = 20, choices=STATUS_CHOICES, default='New')
    admin_notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.reportTitle
    
class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["user", "reportTitle", "reportDescription", "reportText", "reportPDF", "reportJPEG"]


