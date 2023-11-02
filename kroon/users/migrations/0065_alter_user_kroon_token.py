# Generated by Django 3.2.9 on 2022-03-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0064_alter_user_kroon_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='kroon_token',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='The customers available kroon token for the account', max_digits=300, null=True, verbose_name='Available Kroon Token'),
        ),
    ]