# Generated by Django 3.2.9 on 2022-01-29 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kroon_otp', '0002_auto_20220129_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opts',
            name='user',
            field=models.ForeignKey(blank=True, help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile'),
        ),
    ]
