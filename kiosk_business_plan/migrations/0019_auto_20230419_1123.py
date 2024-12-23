# Generated by Django 3.2.9 on 2023-04-19 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_business_plan', '0018_business_plan_business_expenses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business_plan',
            name='business_expenses',
        ),
        migrations.AddField(
            model_name='business_plan',
            name='business_expenses',
            field=models.ManyToManyField(help_text='this is the business Expenses that is link to the expenses .', related_name='merchant_business_Expenses_profile', to='kiosk_business_plan.BusinessPlanExpenses', verbose_name='Business Expenses'),
        ),
    ]
