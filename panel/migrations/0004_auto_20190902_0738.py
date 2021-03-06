# Generated by Django 2.2.4 on 2019-09-02 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_auto_20190902_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='BOEC',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='HP_Rating',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='Machining_Assembly',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='Software_Level',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='TRANS',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='Truck_Model',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
    ]
