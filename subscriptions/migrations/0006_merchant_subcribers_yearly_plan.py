# Generated by Django 3.2.9 on 2022-06-16 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0005_auto_20220616_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant_subcribers',
            name='yearly_plan',
            field=models.BooleanField(blank=True, default=False, help_text='this indicates that this current plan is meant to be a yearly plan or not ', null=True, verbose_name='Year Plan'),
        ),
    ]