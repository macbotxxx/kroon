# Generated by Django 3.2.9 on 2022-01-14 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kroon_kiosk', '0004_alter_cartitem_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('order_number', models.CharField(help_text='Order generated number to identify the current customer order', max_length=150, null=True, verbose_name='Order Number')),
                ('order_total', models.IntegerField(blank=True, help_text='Total amount for the current order placed by the customer', null=True, verbose_name='Order Total Amount')),
                ('is_ordered', models.BooleanField(blank=True, default=False, help_text='the current state of the order , which identifies if the order is been processed successfully or not.', null=True, verbose_name='Order Operation')),
            ],
            options={
                'verbose_name': 'Kiosk Completed Order',
                'verbose_name_plural': 'Kiosk Completed Order',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('payment_ref', models.CharField(help_text='The payment ref number is an auto generated number from kroon kiosk to store each process by the merchant user be it cash, kroon token and card.', max_length=150, null=True, verbose_name='Payment Ref No')),
                ('payment_method', models.CharField(blank=True, choices=[('kroon token', 'Kroon Token'), ('card payment', 'Card Payment'), ('cash payment', 'Cash Payment')], default='card payment', help_text='The payment method used while paying for an order.', max_length=150, null=True, verbose_name='Payment Method')),
                ('amount_paid', models.IntegerField(help_text='Amount paid for the above order by the customer.', null=True, verbose_name='Amount Paid')),
                ('verified', models.BooleanField(blank=True, default=False, help_text='Verified payment status to identify if the payment is been verified by the payment gateway or not.', null=True, verbose_name='Payment Verification')),
                ('status', models.CharField(help_text='payment status to identify if the payment is been verified by the payment gateway or not.', max_length=150, null=True, verbose_name='Payment Status')),
                ('user', models.ForeignKey(help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='merchant', to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
            ],
            options={
                'verbose_name': 'Kiosk Payment Record',
                'verbose_name_plural': 'Kiosk Payment Record',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('quantity', models.IntegerField(blank=True, help_text='product quantity for the current product been order by the customer.', null=True, verbose_name='Product Quantity')),
                ('ordered', models.BooleanField(blank=True, default=False, help_text='the current state of the order , which identifies if the order is been processed successfully or not.', null=True, verbose_name='Order Operation')),
                ('order', models.ForeignKey(blank=True, help_text='foreign key and session to the order table.', null=True, on_delete=django.db.models.deletion.CASCADE, to='kroon_kiosk.order')),
                ('payment', models.ForeignKey(blank=True, help_text='foreign key and session to the payment table.', null=True, on_delete=django.db.models.deletion.CASCADE, to='kroon_kiosk.payment')),
                ('product', models.ForeignKey(blank=True, help_text='foreign key and session to the product table.', null=True, on_delete=django.db.models.deletion.CASCADE, to='kroon_kiosk.product')),
                ('user', models.ForeignKey(help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
            ],
            options={
                'verbose_name': 'Kiosk Ordered Products',
                'verbose_name_plural': 'Kiosk Ordered Products',
                'ordering': ('-created_date',),
            },
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, help_text='Customers order payment information.', null=True, on_delete=django.db.models.deletion.CASCADE, to='kroon_kiosk.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(help_text='The user for whom account belongs to', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User Profile'),
        ),
    ]
