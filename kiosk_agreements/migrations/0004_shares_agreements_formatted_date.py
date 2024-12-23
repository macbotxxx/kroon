# Generated by Django 4.1.9 on 2023-06-23 11:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kiosk_agreements", "0003_alter_goods_and_services_agreement_price_of_good_and_service_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="shares_agreements",
            name="formatted_date",
            field=models.DateField(
                help_text="The date is formatted to when the agreement is taken.",
                null=True,
                verbose_name="Formatted Date",
            ),
        ),
    ]
