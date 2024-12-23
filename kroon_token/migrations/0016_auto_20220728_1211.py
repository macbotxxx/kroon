# Generated by Django 3.2.9 on 2022-07-28 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_language'),
        ('kroon_token', '0015_alter_withdrawtokenfees_withdrawal_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasetokenfees',
            name='country',
            field=models.ForeignKey(blank=True, help_text='The country residence of the customer. KYC verification will be applied to this country and customer must provide proof of such residence as relevant in the country of jurisdiction.', null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.country', verbose_name='Country of Residence'),
        ),
        migrations.AlterField(
            model_name='withdrawtokenfees',
            name='country',
            field=models.ForeignKey(blank=True, help_text='The country residence of the customer. KYC verification will be applied to this country and customer must provide proof of such residence as relevant in the country of jurisdiction.', null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.country', verbose_name='Country of Residence'),
        ),
    ]
