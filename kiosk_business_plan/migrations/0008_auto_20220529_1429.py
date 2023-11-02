# Generated by Django 3.2.9 on 2022-05-29 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk_business_plan', '0007_alter_business_plan_year_of_operation'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_plan',
            name='data',
            field=models.IntegerField(default=0, help_text='the initiated amount you paid for internet data bills monthly.', null=True, verbose_name='Internet Data Bill'),
        ),
        migrations.AddField(
            model_name='business_plan',
            name='electricity',
            field=models.IntegerField(default=0, help_text='the initiated amount you paid for electricity bill monthly.', null=True, verbose_name='Electricity Bills'),
        ),
        migrations.AddField(
            model_name='business_plan',
            name='fuel',
            field=models.IntegerField(default=0, help_text='the initiated amount you paid for fuel monthly.', null=True, verbose_name='Fuel Bill'),
        ),
        migrations.AddField(
            model_name='business_plan',
            name='salaries',
            field=models.IntegerField(default=0, help_text='the amount of salary that your workers is been paid monthly', null=True, verbose_name='Salaries'),
        ),
    ]