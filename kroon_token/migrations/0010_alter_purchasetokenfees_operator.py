# Generated by Django 3.2.9 on 2022-02-10 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroon_token', '0009_auto_20220208_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasetokenfees',
            name='operator',
            field=models.CharField(choices=[('card topup', 'Card Topup'), ('agent topup', 'Agent TopUp')], help_text='this section hold the operator which the current fees should be applied to.', max_length=300, null=True, verbose_name='Operators'),
        ),
    ]