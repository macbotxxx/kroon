# Generated by Django 3.2.9 on 2022-01-23 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0040_auto_20220123_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrequesttoken',
            name='action',
            field=models.CharField(default='KROON TOKEN REQUEST', editable=False, help_text='action status for the current transaction.', max_length=20, null=True, verbose_name='Action'),
        ),
    ]
