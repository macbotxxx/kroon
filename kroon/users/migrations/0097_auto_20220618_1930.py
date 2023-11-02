# Generated by Django 3.2.9 on 2022-06-18 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0096_remove_businessprofile_web_dark_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='kroontermsandconditions',
            name='platform',
            field=models.CharField(blank=True, choices=[('kroon', 'kroon'), ('kiosk', 'kiosk')], help_text='this indicates the platform which the teams and conditions is been generated for.', max_length=255, null=True, verbose_name='Platform'),
        ),
        migrations.AddField(
            model_name='policyandcondition',
            name='platform',
            field=models.CharField(blank=True, choices=[('kroon', 'kroon'), ('kiosk', 'kiosk')], help_text='this indicates the platform which the policy is been generated for.', max_length=255, null=True, verbose_name='Platform'),
        ),
    ]