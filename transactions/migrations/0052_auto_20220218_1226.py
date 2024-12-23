# Generated by Django 3.2.9 on 2022-02-18 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0051_auto_20220217_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kroontokenrequest',
            name='action',
            field=models.CharField(default='KROON REQUEST', editable=False, help_text='action status for the current transaction.', max_length=300, null=True, verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='userrequesttoken',
            name='action',
            field=models.CharField(default='KROON REQUEST', editable=False, help_text='action status for the current transaction.', max_length=20, null=True, verbose_name='Action'),
        ),
    ]
