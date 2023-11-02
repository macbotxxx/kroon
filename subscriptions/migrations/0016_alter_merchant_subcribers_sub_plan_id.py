# Generated by Django 4.1.9 on 2023-06-06 12:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0015_alter_merchant_subcribers_sub_plan_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="merchant_subcribers",
            name="sub_plan_id",
            field=models.CharField(
                blank=True,
                help_text="this plan id holds the id given to identify the subscription plan of the user which cna be the yearly plan id or the monthly plan id",
                max_length=255,
                null=True,
                verbose_name="Sub Plan ID",
            ),
        ),
    ]