# Generated by Django 3.2.9 on 2022-06-12 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0094_auto_20220612_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessprofile',
            name='business_default_language',
            field=models.CharField(help_text='the merchant default langauge for his business profile', max_length=255, null=True, verbose_name='Business Default Language'),
        ),
    ]
