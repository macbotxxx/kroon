# Generated by Django 3.2.9 on 2022-03-24 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0066_alter_transactions_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='card',
            field=models.BooleanField(blank=True, default=False, help_text='this indicates whether the transaction is been paid using card, if so the card details will be saved.', null=True, verbose_name='Card Transaction Status'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='card_country',
            field=models.CharField(blank=True, help_text='this shows the country in which the user card is been provided from or issued to the user.', max_length=50, null=True, verbose_name='Card Country'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='card_expiry',
            field=models.CharField(blank=True, help_text='the expiring date of the user card will be store here.', max_length=300, null=True, verbose_name='Card Expiry'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='card_first_6digits',
            field=models.IntegerField(blank=True, help_text='the fields store the user card first 6 digits used for the transaction charge.', null=True, verbose_name='Card First 6 digits'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='card_issuer',
            field=models.CharField(blank=True, help_text='the fields store the user card issuer , for easy identification.', max_length=300, null=True, verbose_name='Card Issuer'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='card_last_4digits',
            field=models.IntegerField(blank=True, help_text='the fields store the user card last 4 digits used for the transaction charge.', null=True, verbose_name='Card Last 4 digits'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='card_type',
            field=models.CharField(blank=True, help_text='this shows the type of card which the user used for this current transaction.', max_length=300, null=True, verbose_name='Card Type'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='device_fingerprint',
            field=models.CharField(blank=True, help_text='the device finger print will be provided by kroon third party , note this is an optional field', max_length=300, null=True, verbose_name='Device Fingerprint'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='flw_ref',
            field=models.CharField(blank=True, editable=False, help_text='the theird party ref is the transactional ref which is generated by kroon topup thrid party.', max_length=355, null=True, verbose_name='Third Party Ref'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, help_text='the ip address of the user when initiated the transaction , note this will be provided by the thrid party providers.', null=True, verbose_name='IP Address'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='payment_type',
            field=models.CharField(blank=True, help_text='the payment type which will be provided by the third party after the transaction has been approved.', max_length=300, null=True, verbose_name='Payment Type'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='transactional_date',
            field=models.DateTimeField(blank=True, help_text='the transactional date which holds the date the transaction was taken by our thrid party providers.', null=True, verbose_name='Transactional Date'),
        ),
    ]