# Generated by Django 4.1.9 on 2023-06-01 09:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0013_merchant_subcribers_device_type_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription_plan",
            name="gov_yearly_plan_fee",
        ),
    ]