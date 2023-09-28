# Generated by Django 3.2.9 on 2022-01-29 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0048_delete_opts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='device_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='firebase_token',
        ),
        migrations.AddField(
            model_name='user',
            name='accept_terms',
            field=models.BooleanField(default=False, help_text='this indicates whether the user accepted kroon terms and conditions.', null=True, verbose_name='Accept Terms'),
        ),
        migrations.AddField(
            model_name='user',
            name='agreed_to_data_usage',
            field=models.BooleanField(default=False, help_text='this indicates whether the user accepted kroon to data usage or not.', null=True, verbose_name='Agree To Data Usage'),
        ),
        migrations.AddField(
            model_name='user',
            name='email_verification',
            field=models.BooleanField(default=False, help_text='this indicates whether the users email verification is been verified or not', null=True, verbose_name='Email Verification'),
        ),
    ]
