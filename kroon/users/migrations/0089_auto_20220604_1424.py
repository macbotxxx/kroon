# Generated by Django 3.2.9 on 2022-06-04 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_categories', '0001_initial'),
        ('users', '0088_businessprofile_business_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessprofile',
            name='business_category',
        ),
        migrations.AddField(
            model_name='businessprofile',
            name='business_category',
            field=models.ManyToManyField(blank=True, help_text='this shows the business category which the user will select from ', null=True, to='kiosk_categories.Category'),
        ),
    ]
