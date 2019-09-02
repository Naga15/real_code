from django.db import models
from django.contrib.auth.models import User
import uuid

#CEPData
class CEPData(models.Model):
    token                           = models.UUIDField(default= uuid.uuid4)
    ESN                             = models.CharField(unique=True, max_length=255,default='')
    Chassis                         = models.CharField(unique=True, max_length=255,default='')
    Engine_Family                   = models.CharField(max_length=255,default='')
    Model_Year                      = models.CharField(max_length=255,default='')
    BOEC                            = models.TextField(blank = True, null=True)
    HP_Rating                       = models.TextField(blank = True, null=True)
    Truck_Model                     = models.CharField(max_length=255,default='')
    Current_Software_Level          = models.TextField(blank = True, null=True)
    Last_Software_Level             = models.TextField(blank = True, null=True)
    publish                         = models.BooleanField(default=True)
    CreatedAt                       = models.DateTimeField(auto_now_add=True, null=True)
    UpdatedAt                       = models.DateTimeField(auto_now=True, null=True)
    
    def __int__(self):
        return self.id

    def __str__(self):
        return str(self.Chassis)

    class Meta:
        verbose_name = 'CEPData'
        verbose_name_plural = 'CEPDatas'

#PlantData
class PlantData(models.Model):
    token                           = models.UUIDField(default= uuid.uuid4)
    CEPData                         = models.ForeignKey(CEPData, on_delete=models.CASCADE,null=True)
    Transmission_Configuration      = models.TextField(blank = True, null=True)
    Application                     = models.TextField(blank = True, null=True)
    Mileage                         = models.CharField(max_length=255,default='')
    After_Treatment_Softwate_Level  = models.TextField(blank = True, null=True)
    Rear_Axle_Ratio                 = models.CharField(max_length=255,default='')
    publish                         = models.BooleanField(default=True)
    CreatedAt                       = models.DateTimeField(auto_now_add=True, null=True)
    UpdatedAt                       = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'PlantData'
        verbose_name_plural = 'PlantDatas'

#SLCase
class SLCase(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    SLID        = models.CharField(unique=True, max_length=255,default='')
    Disposition = models.TextField(blank = True, null=True)
    Message     = models.TextField(blank = True, null=True)
    publish     = models.BooleanField(default=True)
    CreatedAt   = models.DateTimeField(auto_now_add=True, null=True)
    UpdatedAt   = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'SLCase'
        verbose_name_plural = 'SLCases'

#Attachments
class Attachments(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    SLCase      = models.ForeignKey(SLCase, on_delete=models.CASCADE,null=True)
    File_Name   = models.CharField(max_length=255,default='')
    File_Type   = models.CharField(max_length=255,default='')
    File_Size   = models.CharField(max_length=255,default='')
    File        = models.FileField(upload_to='uploads/')
    Description = models.TextField(blank = True, null=True)
    publish     = models.BooleanField(default=True)
    CreatedAt   = models.DateTimeField(auto_now_add=True, null=True)
    UpdatedAt   = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'