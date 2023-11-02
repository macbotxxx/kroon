# Generated by Django 3.2.9 on 2021-12-18 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], help_text='the gender that is allowed to view this ad', max_length=8, null=True, verbose_name='Gender'),
        ),
    ]