# Generated by Django 4.2.5 on 2023-10-11 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("locations", "0006_auto_20221212_1021"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminPushNotifications",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="The unique identifier of an object.",
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="Timestamp when the record was created.",
                        max_length=20,
                        verbose_name="Created Date",
                    ),
                ),
                (
                    "modified_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="Modified date when the record was created.",
                        max_length=20,
                        verbose_name="Modified Date",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="The title of the new feed that will be displayed to the user",
                        max_length=255,
                        null=True,
                        verbose_name="News Feed Title",
                    ),
                ),
                (
                    "device_id",
                    models.CharField(
                        help_text="this stores the device ID of the merchants device which is linked to their account",
                        max_length=150,
                        null=True,
                        verbose_name="Device ID",
                    ),
                ),
                (
                    "body_message",
                    models.TextField(
                        help_text="this holds the content of the push notification",
                        null=True,
                        verbose_name="Body Message",
                    ),
                ),
                (
                    "platform",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("all_the_above", "all_the_above"),
                            ("kroon", "kroon"),
                            ("kroon kiosk", "kroon_kiosk"),
                        ],
                        default="all_the_above",
                        help_text="The platform that is only valid to view this news feed specified for the paltform only , which can also be identified as the 'all the above' which shows all the contents for kroon and kroon kiosk to the users",
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "device_type",
                    models.CharField(
                        help_text="this storess the device type in which the push notifications is been sent to",
                        max_length=25,
                        null=True,
                        verbose_name="Device Type",
                    ),
                ),
                (
                    "notification_type",
                    models.CharField(
                        help_text="the notification type is the type of notification that is been sent by the admin",
                        max_length=25,
                        null=True,
                        verbose_name="Notification Type",
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=False,
                        help_text="news feed status which determines whether the feed should be shown or not",
                        null=True,
                        verbose_name="News Feed Status",
                    ),
                ),
                (
                    "news_feed_country",
                    models.ManyToManyField(
                        help_text="The country that is only valid to view this news feed ",
                        to="locations.country",
                        verbose_name="News Feed Country",
                    ),
                ),
                (
                    "publisher",
                    models.ForeignKey(
                        blank=True,
                        help_text="This holds the publisher name ",
                        max_length=255,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Publisher",
                    ),
                ),
            ],
            options={
                "verbose_name": "Push Notification",
                "verbose_name_plural": "Push Notification",
                "ordering": ("-created_date",),
            },
        ),
    ]
