# Generated by Django 4.2.3 on 2023-08-07 23:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gov_panel", "0007_rename_government_organization_name_government_organizations_government_organization"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="government_organizations",
            options={"verbose_name": "Government Organizations", "verbose_name_plural": "Government Organizations"},
        ),
        migrations.RemoveField(
            model_name="government_organizations",
            name="created_date",
        ),
        migrations.RemoveField(
            model_name="government_organizations",
            name="modified_date",
        ),
    ]
