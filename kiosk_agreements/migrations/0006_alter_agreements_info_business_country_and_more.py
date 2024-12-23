# Generated by Django 4.1.9 on 2023-06-23 13:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kiosk_agreements", "0005_agreements_info_employee_signature_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="agreements_info",
            name="business_country",
            field=models.CharField(
                help_text="The business Country in which the business operates.",
                max_length=200,
                null=True,
                verbose_name="Business Country",
            ),
        ),
        migrations.AlterField(
            model_name="goods_and_services_agreement",
            name="buyer_country",
            field=models.CharField(
                help_text="The Buyer Country in which the business operates.",
                max_length=200,
                null=True,
                verbose_name="Buyer Country",
            ),
        ),
        migrations.AlterField(
            model_name="goods_and_services_agreement",
            name="seller_country",
            field=models.CharField(
                help_text="The seller Country in which the seller operates.",
                max_length=200,
                null=True,
                verbose_name="Seller Country",
            ),
        ),
        migrations.AlterField(
            model_name="loan_agreement",
            name="lender_country",
            field=models.CharField(
                help_text="The lender Country in which the business operates.",
                max_length=200,
                null=True,
                verbose_name="Lender Country",
            ),
        ),
        migrations.AlterField(
            model_name="shares_agreements",
            name="company_country",
            field=models.CharField(
                help_text="The company Country in which the company operates.",
                max_length=200,
                null=True,
                verbose_name="Company Country",
            ),
        ),
    ]
