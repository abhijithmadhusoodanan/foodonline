# Generated by Django 4.1.1 on 2025-01-28 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='vednor_name',
            new_name='vendor_name',
        ),
    ]
