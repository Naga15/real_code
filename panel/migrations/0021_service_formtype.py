# Generated by Django 2.2.5 on 2019-09-25 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0020_auto_20190903_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='FormType',
            field=models.CharField(choices=[('CEP', 'CEP Data'), ('Plant', 'Plant Data'), ('Case', 'Case'), ('Claim', 'Claim Info'), ('Davie', 'Davie Logs'), ('Fault', 'Fault Codes')], default=0, max_length=20),
        ),
    ]
