# Generated by Django 3.2.9 on 2022-03-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kroon_gift', '0004_alter_kroongift_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kroongift',
            name='amount',
            field=models.DecimalField(decimal_places=2, help_text='the amount in kroon token to be sent the user.', max_digits=300, null=True, verbose_name='Amount In Kroon'),
        ),
    ]
