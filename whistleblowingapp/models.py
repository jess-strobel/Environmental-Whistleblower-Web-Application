from django.db import models

FILE_TYPES = (
    ('txt', 'Text File'),
    ('pdf', 'PDF'),
    ('jpg', 'JPEG Image'),
)

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
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    file_type = models.CharField(max_length=3, choices=FILE_TYPES)
    attachment = models.FileField(upload_to='report_attachments/')
    def __str__(self):
        return self.title