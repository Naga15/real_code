# Generated by Django 2.2.4 on 2019-09-02 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0004_auto_20190902_0738'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='TRANS',
            new_name='Transmission_Configuration',
        ),
    ]
