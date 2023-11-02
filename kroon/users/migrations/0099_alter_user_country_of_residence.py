# Generated by Django 3.2.9 on 2022-07-28 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_language'),
        ('users', '0098_auto_20220728_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country_of_residence',
            field=models.ForeignKey(blank=True, help_text='The country residence of the customer. KYC verification will be applied to this country and customer must provide proof of such residence as relevant in the country of jurisdiction.', null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.country', verbose_name='Country of Residence'),
        ),
    ]