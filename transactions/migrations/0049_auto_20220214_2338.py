# Generated by Django 3.2.9 on 2022-02-14 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0048_auto_20220207_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequesttoken',
            name='accepted_status',
            field=models.BooleanField(blank=True, default=False, help_text='this is hold the status bar that determines if the transaction was accepted or not.', null=True, verbose_name='Accepted Status'),
        ),
        migrations.AlterField(
            model_name='kroontokenrequest',
            name='action',
            field=models.CharField(default='OPEN KROON TOKEN REQUEST', editable=False, help_text='action status for the current transaction.', max_length=300, null=True, verbose_name='Action'),
        ),
    ]
