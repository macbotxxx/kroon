# Generated by Django 3.2.9 on 2022-08-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0011_alter_ads_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='platform',
            field=models.CharField(choices=[('all_the_above', 'all_the_above'), ('kroon', 'Kroon'), ('kiosk', 'Kiosk')], default='all_the_above', help_text='the gender that is allowed to view this ad', max_length=30, null=True, verbose_name='Ad Platform'),
        ),
    ]
