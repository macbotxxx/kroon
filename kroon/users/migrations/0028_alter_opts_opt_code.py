# Generated by Django 3.2.9 on 2021-12-24 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_alter_opts_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opts',
            name='opt_code',
            field=models.CharField(help_text='opt code that will be sent to the user for validation and resting of transactional pin.', max_length=6, null=True, verbose_name='Opt Code'),
        ),
    ]
