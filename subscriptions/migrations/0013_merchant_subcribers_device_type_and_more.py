# Generated by Django 4.1.9 on 2023-06-01 01:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0012_subscription_plan_gov_yearly_plan_fee"),
    ]

    operations = [
        migrations.AddField(
            model_name="merchant_subcribers",
            name="device_type",
            field=models.CharField(
                blank=True,
                help_text="this indicates the merchants device type , ether its an apple or google device type",
                max_length=25,
                null=True,
                verbose_name="Device Type",
            ),
        ),
        migrations.AddField(
            model_name="merchant_subcribers",
            name="receipt_data",
            field=models.TextField(
                blank=True,
                help_text="The token provided to the user's device when the subscription was purchased.",
                null=True,
                verbose_name=" Receipt Data ",
            ),
        ),
        migrations.AddField(
            model_name="subscription_plan",
            name="slug_plan_name",
            field=models.CharField(
                blank=True,
                help_text="the will be the subscription plan, provided by the admin ",
                max_length=50,
                null=True,
                verbose_name="Sulg Plan Name",
            ),
        ),
    ]