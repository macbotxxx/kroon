# Generated by Django 3.2.9 on 2022-02-02 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_money', '0004_mobilemoneytopup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobilemoneyaccount',
            name='network',
            field=models.ForeignKey(blank=True, default='MPS', help_text='mobile money network providers which is only accepted for countries like Ghana, Zambia.', null=True, on_delete=django.db.models.deletion.CASCADE, to='mobile_money.networkprovider'),
        ),
    ]
