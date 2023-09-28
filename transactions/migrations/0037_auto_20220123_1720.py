# Generated by Django 3.2.9 on 2022-01-23 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0036_alter_kroontokentransfer_action'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kroontokenrequest',
            name='request_user',
        ),
        migrations.AddField(
            model_name='kroontokenrequest',
            name='recipient',
            field=models.ForeignKey(help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Recipient User Profile'),
        ),
        migrations.AlterField(
            model_name='kroontokentransfer',
            name='recipient',
            field=models.ForeignKey(help_text='The user for whom account belongs to', on_delete=django.db.models.deletion.PROTECT, related_name='reciever', to=settings.AUTH_USER_MODEL, verbose_name='Recipient Profile'),
        ),
    ]
