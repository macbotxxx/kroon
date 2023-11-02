# Generated by Django 3.2.9 on 2022-01-23 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0039_auto_20220123_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrequesttoken',
            name='request_user',
        ),
        migrations.AddField(
            model_name='userrequesttoken',
            name='recipient',
            field=models.ForeignKey(help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Request User Profile'),
        ),
    ]