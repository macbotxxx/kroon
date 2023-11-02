# Generated by Django 3.2.9 on 2022-07-25 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0010_alter_ads_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='platform',
            field=models.CharField(choices=[('kroon', 'Kroon'), ('kiosk', 'Kiosk')], help_text='the gender that is allowed to view this ad', max_length=8, null=True, verbose_name='Ad Platform'),
        ),
    ]