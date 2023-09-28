# Generated by Django 3.2.9 on 2022-06-03 22:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscriptions', '0004_alter_merchant_subcribers_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Government_Promo_Code',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('promo_code', models.CharField(blank=True, help_text='the promotional code which represents the code for the given plan , this code activates the plan when is not used.', max_length=255, null=True, verbose_name='Promo Code')),
                ('used_code', models.BooleanField(default=False, help_text='this hsows if the code is been used by another customer or already expired.', null=True, verbose_name='Used Code')),
                ('code_plan', models.ForeignKey(blank=True, help_text='gthe code plans represents the plan in which the promotional code will be linked to', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='code_plans', to='subscriptions.subscription_plan')),
            ],
            options={
                'verbose_name': 'Government Promo Code',
                'verbose_name_plural': 'Government Promo Code',
                'ordering': ('-created_date',),
            },
        ),
    ]
