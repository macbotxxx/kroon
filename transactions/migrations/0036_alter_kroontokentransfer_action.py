# Generated by Django 3.2.9 on 2022-01-23 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0035_alter_kroontokentransfer_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kroontokentransfer',
            name='action',
            field=models.CharField(default='KROON TOKEN TRANSFER', editable=False, help_text='action status for the current transaction.', max_length=300, null=True, verbose_name='Action'),
        ),
    ]
