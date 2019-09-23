from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from datetime import date

#CEPData
class CEPData(models.Model):
    token                           = models.UUIDField(default= uuid.uuid4)
    ESN                             = models.CharField(unique=True, max_length=255,default='')
    Chassis                         = models.CharField(unique=True, max_length=255,default='')
    Engine_Date                     = models.DateField(default=date.today)
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
    cep                             = models.OneToOneField(CEPData,on_delete=models.CASCADE,primary_key=True)
    token                           = models.UUIDField(default= uuid.uuid4)
    Transmission_Configuration      = models.CharField(max_length=255,blank = True, null=True)
    Application                     = models.CharField(max_length=255,blank = True, null=True)
    Mileage                         = models.CharField(max_length=255,blank = True, null=True)
    After_Treatment_Softwate_Level  = models.CharField(max_length=255,blank = True, null=True)
    Rear_Axle_Ratio                 = models.CharField(max_length=255,blank = True, null=True)
    publish                         = models.BooleanField(default=True)
    CreatedAt                       = models.DateTimeField(auto_now_add=True, null=True)
    UpdatedAt                       = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'PlantData'
        verbose_name_plural = 'PlantDatas'

#Service
class Service(models.Model):
    cep                             = models.ForeignKey(CEPData,on_delete=models.CASCADE)
    token                           = models.UUIDField(default= uuid.uuid4)
    FormType                        = models.CharField(max_length=20, choices=(('CEP','CEP Data'),('Plant','Plant Data'),('Case','Case'),('Claim','Claim Info'),('Davie','Davie Logs'),('Fault','Fault Codes')),  default=0)
    Service_Date                    = models.DateField(default=date.today)
    Mileage                         = models.IntegerField(blank = True, null=True)
    publish                         = models.BooleanField(default=True)
    CreatedAt                       = models.DateTimeField(auto_now_add=True, null=True)
    UpdatedAt                       = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'services'

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
class Attachment(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    SLCase      = models.ForeignKey(SLCase, on_delete=models.CASCADE,null=True)
    Attachment  = models.FileField(upload_to='uploads/')
    Type_Code   = models.CharField(max_length=255,default='')
    Description = models.TextField(blank = True, null=True)
    publish     = models.BooleanField(default=True)
    CreatedAt   = models.DateTimeField(auto_now_add=True, null=True)
    UpdatedAt   = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'


#Claims
class Claim(models.Model):
    token           = models.UUIDField(default= uuid.uuid4)
    publish         = models.BooleanField(default=True)
    Dealer_Story    = models.TextField(blank = True, null=True)
    Cost_Parts      = models.CharField(max_length=255,blank = True, null=True)
    Cost_Labor      = models.CharField(max_length=255,blank = True, null=True)
    Cost_Total      = models.CharField(max_length=255,blank = True, null=True)
    PR_Part_No      = models.CharField(max_length=255,blank = True, null=True)
    PR_Part_Desc    = models.CharField(max_length=255,blank = True, null=True)
    PR_Part_Amount  = models.CharField(max_length=255,blank = True, null=True)
    Part_Source     = models.CharField(max_length=255,blank = True, null=True)
    Quantity        = models.CharField(max_length=255,blank = True, null=True)
    Campaign        = models.CharField(max_length=255,blank = True, null=True)
    Bulletin        = models.CharField(max_length=255,blank = True, null=True)
    CreatedAt       = models.DateTimeField(auto_now_add=True, null=True)
    UpdatedAt       = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'Claim'
        verbose_name_plural = 'Claims'

#Davie Logs
class Davie_Log(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    publish     = models.BooleanField(default=True)
    Attachment  = models.FileField(upload_to='uploads/',blank = True, null=True)
    CreatedAt   = models.DateTimeField(auto_now_add=True, null=True)
    UpdatedAt   = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'Davie Log'
        verbose_name_plural = 'Davie Logs'

#Fault Codes
class Fault_Code(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    P_Code      = models.CharField(max_length=255,default='')
    Title       = models.CharField(max_length=255,default='')
    Mileage     = models.CharField(max_length=255,default='')
    publish     = models.BooleanField(default=True)
    CreatedAt   = models.DateTimeField(auto_now_add=True, null=True)
    UpdatedAt   = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'Fault Code'
        verbose_name_plural = 'Fault Codes'