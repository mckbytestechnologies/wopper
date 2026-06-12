from django.db import models
from config import app_gv as gv
from django_countries.fields import CountryField
from django.conf import settings
from django_countries.fields import CountryField





class VersionControl(models.Model):
    app = models.CharField(choices=gv.APP_LIST, default='CUS_ANDROID_APP', max_length=100)
    version = models.CharField(max_length=10)
    released_on = models.DateTimeField(auto_now_add=True)
    datamode = models.CharField(max_length=5, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'version_control'

    def __str__(self):
        return "{0}-{1}".format(self.app, self.version)


class MasterPermission(models.Model):
    app_name = models.CharField(max_length=255, db_index=True) # App Name
    class_name = models.CharField(max_length=255, unique=True, db_index=True) # Class Name
    module_name = models.CharField(max_length=255)
    function_name = models.CharField(max_length=255) # Read, Update, delete, btn action
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    def __str__(self):
        return f"{self.class_name} - {self.function_name}"

    class Meta:
        db_table = 'master_permission'