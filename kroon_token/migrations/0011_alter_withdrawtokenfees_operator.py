# Generated by Django 3.2.9 on 2022-02-23 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroon_token', '0010_alter_purchasetokenfees_operator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawtokenfees',
            name='operator',
            field=models.CharField(choices=[('bank withdrawal', 'Bank Withdrawal'), ('agent cashout', 'Agent Cashout'), ('mobile money cashout', 'Mobile Money Cashout')], help_text='this section hold the withdrawal operator which the current fees should be applied to.', max_length=300, null=True, verbose_name='Withdraw Operators'),
        ),
    ]
