# Generated by Django 3.2.9 on 2022-03-14 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroon_kyc', '0012_alter_marchantkycapplication_business_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kycapplication',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='kycapplication',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='marchantkycapplication',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='marchantkycapplication',
            name='address_line_2',
        ),
        migrations.AddField(
            model_name='kycapplication',
            name='building_name',
            field=models.CharField(blank=True, help_text='Building Name of the user', max_length=50, null=True, verbose_name='Building Name'),
        ),
        migrations.AddField(
            model_name='kycapplication',
            name='street_name',
            field=models.CharField(blank=True, help_text='Street Name of the user', max_length=50, null=True, verbose_name='Street Name'),
        ),
        migrations.AddField(
            model_name='kycapplication',
            name='street_or_flat_number',
            field=models.CharField(blank=True, help_text='Street or Flat Number"), of the user', max_length=50, null=True, verbose_name='Street or Flat Number'),
        ),
        migrations.AddField(
            model_name='marchantkycapplication',
            name='building_name',
            field=models.CharField(blank=True, help_text='Building Name of the user', max_length=50, null=True, verbose_name='Building Name'),
        ),
        migrations.AddField(
            model_name='marchantkycapplication',
            name='street_name',
            field=models.CharField(blank=True, help_text='Street Name of the user', max_length=50, null=True, verbose_name='Street Name'),
        ),
        migrations.AddField(
            model_name='marchantkycapplication',
            name='street_or_flat_number',
            field=models.CharField(blank=True, help_text='Street or Flat Number"), of the user', max_length=50, null=True, verbose_name='Street or Flat Number'),
        ),
    ]