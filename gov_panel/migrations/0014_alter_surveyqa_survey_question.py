# Generated by Django 4.2.3 on 2023-08-10 12:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gov_panel", "0013_app_survey_surveyqa"),
    ]

    operations = [
        migrations.AlterField(
            model_name="surveyqa",
            name="survey_question",
            field=models.CharField(
                blank=True,
                help_text="the hold the answer of the survey",
                max_length=250,
                null=True,
                verbose_name="Survey Answer",
            ),
        ),
    ]
