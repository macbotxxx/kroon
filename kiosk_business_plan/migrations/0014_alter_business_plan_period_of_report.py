# Generated by Django 3.2.9 on 2022-06-17 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_business_plan', '0013_alter_business_plan_business_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_plan',
            name='period_of_report',
            field=models.CharField(choices=[('12', '1 Year'), ('24', '2 Year'), ('36', '3 Year')], help_text='Select the how mnay months report you want to generate for your business', max_length=255, null=True, verbose_name='Period Of Report'),
        ),
    ]
