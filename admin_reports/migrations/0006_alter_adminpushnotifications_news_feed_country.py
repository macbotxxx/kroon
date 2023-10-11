# Generated by Django 4.2.5 on 2023-10-11 16:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0006_auto_20221212_1021"),
        ("admin_reports", "0005_alter_adminpushnotifications_news_feed_country_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adminpushnotifications",
            name="news_feed_country",
            field=models.ManyToManyField(
                help_text="The country that is only valid to view this news feed ",
                to="locations.country",
                verbose_name="News Feed Country",
            ),
        ),
    ]
