# Generated by Django 3.2.9 on 2022-07-28 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0010_merchant_subcribers_sub_plan_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant_subcribers',
            name='user',
            field=models.ForeignKey(help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_subcribers', to=settings.AUTH_USER_MODEL, verbose_name='User Profile'),
        ),
    ]
