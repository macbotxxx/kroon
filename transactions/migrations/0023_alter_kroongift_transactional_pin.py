# Generated by Django 3.2.9 on 2021-12-24 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0022_auto_20211224_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kroongift',
            name='transactional_pin',
            field=models.CharField(help_text='Transaction pin that belongs ', max_length=6, null=True, verbose_name='Transactional Pin'),
        ),
    ]
