from django.contrib import admin
from .models import *
from django import forms

'''
class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = ('ESN','Chassis','Engine_Family')
    
    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
      
class VehicleAdmin(admin.ModelAdmin):
    
    form = VehicleForm
    
    #make publish Question
    def make_published(self, request, queryset):
        rows_updated = queryset.update(publish=True)
        if rows_updated == 1:
            message_bit = "1 Vehicle was"
        else:
            message_bit = "%s vehicles were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    make_published.short_description = "Mark selected vehicles as published"    

    #make unpublish country
    def make_unpublished(self, request, queryset):
        rows_updated = queryset.update(publish=False)
        if rows_updated == 1:
            message_bit = "1 Vehicle was"
        else:
            message_bit = "%s vehicles were" % rows_updated
        self.message_user(request, "%s successfully marked as unpublished." % message_bit)

    make_unpublished.short_description = "Mark selected vehicles as unpublished"    

    #field list
    list_display = ('ESN','Chassis','publish')
    list_filter =('publish',)
    search_fields = ('ESN','Chassis')
    actions = [make_published,make_unpublished]

admin.site.register(Vehicle, VehicleAdmin)
'''

admin.site.register(CEPData)
admin.site.register(PlantData)
admin.site.register(SLCase)
admin.site.register(Attachments)