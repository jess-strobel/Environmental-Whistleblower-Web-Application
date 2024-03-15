from django.db import models

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
    reportTitle = models.CharField(max_length=255)
    reportText = models.FileField(upload_to='report_txt/', blank=True, null=True)
    reportPDF = models.FileField(upload_to='report_pdf/', blank=True, null=True)
    reportJPEG = models.ImageField(upload_to='report_image/', blank=True, null=True)

    def __str__(self):
        return self.reportTitle