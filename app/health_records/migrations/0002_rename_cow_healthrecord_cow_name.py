# Generated by Django 4.1.13 on 2025-01-20 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_records', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='healthrecord',
            old_name='cow',
            new_name='cow_name',
        ),
    ]
