# Generated by Django 3.2.9 on 2021-12-19 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0016_transactionalpin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionalpin',
            name='password',
            field=models.IntegerField(help_text='this input holds the user transaction pin which is been hased', null=True, verbose_name='Transactional Pin'),
        ),
    ]
