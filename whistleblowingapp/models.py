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