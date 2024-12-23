# Generated by Django 4.2.5 on 2023-10-11 17:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0006_auto_20221212_1021"),
        ("admin_reports", "0006_alter_adminpushnotifications_news_feed_country"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adminpushnotifications",
            name="news_feed_country",
            field=models.ManyToManyField(
                help_text="The country that is only valid to view this ",
                to="locations.country",
                verbose_name="Country",
            ),
        ),
        migrations.AlterField(
            model_name="adminpushnotifications",
            name="platform",
            field=models.CharField(
                choices=[("all_the_above", "all_the_above"), ("kroon", "kroon"), ("kroon kiosk", "kroon_kiosk")],
                default="all_the_above",
                help_text="This holds the platform that is only valid to recieve the push notification, which can also be identified as the 'all the above' which shows the contents for devices and platforms that is registered under kroon network.",
                max_length=30,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="adminpushnotifications",
            name="title",
            field=models.CharField(
                help_text="The title of the new feed that will be displayed to the user",
                max_length=255,
                null=True,
                verbose_name="Title",
            ),
        ),
    ]
