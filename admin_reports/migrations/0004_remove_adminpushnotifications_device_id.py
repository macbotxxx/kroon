# Generated by Django 4.2.5 on 2023-10-11 16:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("admin_reports", "0003_alter_adminpushnotifications_created_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="adminpushnotifications",
            name="device_id",
        ),
    ]
