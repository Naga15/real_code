# Generated by Django 2.2.4 on 2019-09-03 07:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0012_auto_20190903_0741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cepdata',
            name='Engine_Date',
            field=models.DateField(default=datetime.datetime(2019, 9, 3, 7, 42, 39, 555887)),
        ),
    ]