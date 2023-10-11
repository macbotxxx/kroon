# Generated by Django 4.2.5 on 2023-10-11 13:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("training_cert", "0002_auto_20230426_1027"),
    ]

    operations = [
        migrations.AlterField(
            model_name="training_cert",
            name="created_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                help_text="Timestamp when the record was created. The date and time \n            are displayed in the Timezone from where request is made. \n            e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC",
                verbose_name="Created",
            ),
        ),
        migrations.AlterField(
            model_name="training_cert",
            name="modified_date",
            field=models.DateTimeField(
                auto_now=True,
                help_text="Timestamp when the record was modified. The date and \n            time are displayed in the Timezone from where request \n            is made. e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC\n            ",
                null=True,
                verbose_name="Updated",
            ),
        ),
    ]
