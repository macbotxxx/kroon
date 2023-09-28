# Generated by Django 4.2.3 on 2023-08-07 22:26

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("gov_panel", "0005_delete_convertion_rate"),
    ]

    operations = [
        migrations.CreateModel(
            name="Government_Organizations",
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
                    "government_organization_name",
                    models.CharField(
                        blank=True,
                        help_text="The government organization name holds the title name of the organisation that the merchant business is registered under",
                        max_length=100,
                        null=True,
                        verbose_name="Government Organization Name",
                    ),
                ),
            ],
            options={
                "verbose_name": "Government Organizations",
                "verbose_name_plural": "Government Organizations",
                "ordering": ("-created_date",),
            },
        ),
    ]
