# Generated by Django 3.2.9 on 2022-02-01 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0043_alter_kroontokenrequest_transactional_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactions',
            old_name='message',
            new_name='narration',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='amount_in_kroon_token',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='type',
        ),
        migrations.AddField(
            model_name='transactions',
            name='amount',
            field=models.FloatField(help_text='transactional amount taken by the customer.', null=True, verbose_name='Amount In Kroon Token'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='recipient',
            field=models.ForeignKey(blank=True, help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trans_reciever', to=settings.AUTH_USER_MODEL, verbose_name='Recipient Profile'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='user',
            field=models.ForeignKey(blank=True, help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile'),
        ),
    ]
