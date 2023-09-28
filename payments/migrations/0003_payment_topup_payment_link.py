# Generated by Django 4.2.3 on 2023-09-14 06:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0002_alter_payment_topup_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment_topup",
            name="payment_link",
            field=models.URLField(
                blank=True,
                help_text="this shows the payment url link ,if only the client is set to use the etransac functionalities.",
                null=True,
                verbose_name="Payment Link",
            ),
        ),
    ]
