# Generated by Django 3.2.9 on 2022-03-18 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0063_auto_20220315_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kroontokenrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('cancelled', 'Cancelled'), ('declined', 'Declined'), ('rejected', 'Rejected/Refused'), ('received', 'Received'), ('successful', 'Successful')], default='pending', help_text='action status for the current transaction, which determines if it successful or not.', max_length=20, null=True, verbose_name='Transaction Status'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('cancelled', 'Cancelled'), ('declined', 'Declined'), ('rejected', 'Rejected/Refused'), ('received', 'Received'), ('successful', 'Successful')], default='pending', help_text='payment status to identify if the payment is been verified by the payment gateway or not.', max_length=150, null=True, verbose_name='Payment Status'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('cancelled', 'Cancelled'), ('declined', 'Declined'), ('rejected', 'Rejected/Refused'), ('received', 'Received'), ('successful', 'Successful')], default='pending', help_text='action status for the current transaction, which determines if it successful or not.', max_length=20, null=True, verbose_name='Transaction Status'),
        ),
        migrations.AlterField(
            model_name='userrequesttoken',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('sent', 'Sent'), ('cancelled', 'Cancelled'), ('declined', 'Declined'), ('rejected', 'Rejected/Refused'), ('received', 'Received'), ('successful', 'Successful')], default='pending', help_text='action status for the current transaction, which determines if it successful or not.', max_length=20, null=True, verbose_name='Transaction Status'),
        ),
    ]