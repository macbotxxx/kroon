# Generated by Django 3.2.9 on 2023-04-19 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kiosk_business_plan', '0016_alter_business_plan_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessPlanExpenses',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('expenses', models.CharField(help_text='this input nneeds to have the expenses title ', max_length=255, null=True, verbose_name='Expenses')),
                ('expenses_amount', models.DecimalField(decimal_places=2, default=0.0, help_text='the initiated amount you paid for Expenses Amount monthly.', max_digits=300, null=True, verbose_name='Expenses Amount')),
                ('business_plan', models.ForeignKey(help_text='this is the business plan that is link to the expenses .', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_business_plan_profile', to='kiosk_business_plan.business_plan', verbose_name='Business Plan')),
                ('user', models.ForeignKey(help_text='The user for whom the business plan will be created for.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_business_plan_expenses', to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
            ],
            options={
                'verbose_name': 'Merchant Business Plan Expenses',
                'verbose_name_plural': 'Merchant Business Plan Expenses',
                'ordering': ('-created_date',),
            },
        ),
    ]
