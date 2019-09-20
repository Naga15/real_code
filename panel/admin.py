from django.contrib import admin
from .models import *
from django import forms


class PlantDataForm(forms.ModelForm):
    
    class Meta:
        model = PlantData
        fields = ["Transmission_Configuration","Application","Mileage","After_Treatment_Softwate_Level","Rear_Axle_Ratio"]

    def __init__(self, *args, **kwargs):
        super(PlantDataForm, self).__init__(*args, **kwargs)

class PlantDataInline(admin.TabularInline):
    model           = PlantData
    extra           = 1
    form            = PlantDataForm


class ServiceForm(forms.ModelForm):
    
    class Meta:
        model = Service
        fields = ["FormType","Service_Date","Mileage"]

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)

class ServiceInline(admin.TabularInline):
    model           = Service
    extra           = 0
    form            = ServiceForm
    
class CEPDataForm(forms.ModelForm):

    class Meta:
        model = CEPData
        fields = ('Engine_Date','ESN','Chassis','Engine_Family','Model_Year','BOEC','HP_Rating','Truck_Model','Current_Software_Level','Last_Software_Level')
    
    def __init__(self, *args, **kwargs):
        super(CEPDataForm, self).__init__(*args, **kwargs)
      
class CEPDataAdmin(admin.ModelAdmin):
    
    form = CEPDataForm
    
    #make publish Question
    def make_published(self, request, queryset):
        rows_updated = queryset.update(publish=True)
        if rows_updated == 1:
            message_bit = "1 CEPData was"
        else:
            message_bit = "%s CEPDatas were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    make_published.short_description = "Mark selected CEPDatas as published"    

    #make unpublish country
    def make_unpublished(self, request, queryset):
        rows_updated = queryset.update(publish=False)
        if rows_updated == 1:
            message_bit = "1 CEPData was"
        else:
            message_bit = "%s CEPDatas were" % rows_updated
        self.message_user(request, "%s successfully marked as unpublished." % message_bit)

    make_unpublished.short_description = "Mark selected CEPDatas as unpublished"    

    #field list
    inlines = (PlantDataInline, ServiceInline)
    list_display = ('Engine_Date','ESN','Chassis','publish')
    list_filter =('publish',)
    search_fields = ('ESN','Chassis')
    actions = [make_published,make_unpublished]

admin.site.register(CEPData, CEPDataAdmin)
admin.site.register(PlantData)
admin.site.register(SLCase)
#admin.site.register(Attachments)