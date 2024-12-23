# Generated by Django 4.2.3 on 2023-08-08 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("gov_panel", "0012_alter_government_organizations_government_organization"),
        ("users", "0117_remove_user_government_organization_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="government_organization_name",
            field=models.ForeignKey(
                blank=True,
                help_text="The government organization name holds the title name of the organisation that the merchant business is registered under",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="gov_panel.government_organizations",
                verbose_name="Government Organization Name",
            ),
        ),
    ]
