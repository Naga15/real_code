# Generated by Django 2.2.4 on 2019-09-03 07:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0011_davie_log_fault_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='cepdata',
            name='Engine_Date',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 3, 7, 41, 28, 873056)),
        ),
        migrations.AddField(
            model_name='claim',
            name='Bulletin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='Campaign',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='Cost_Labor',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='Cost_Parts',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='Cost_Total',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='Dealer_Story',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='PR_Part_Amount',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='PR_Part_Desc',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='PR_Part_No',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='Part_Source',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='Quantity',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='davie_log',
            name='Attachment',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='fault_code',
            name='Mileage',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='fault_code',
            name='P_Code',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='fault_code',
            name='Title',
            field=models.CharField(default='', max_length=255),
        ),
    ]
