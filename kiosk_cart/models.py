from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from kroon.users.models import User
from kiosk_stores.models import Merchant_Product, ProductVariation

# Create your models here.


class Payment(BaseModel):
    """
    Payement model for accepting orders.
    """
    PAYMENT_METHOD = (
        ('kroon_token', _('Kroon Token')),
        ('card_payment', _('Card Payment')),
        ('cash_payment', _('Cash Payment')),
        ('mobile_money_payment', _('Mobile Money Payment')),
        ('local_bank_transfer', _('Local Bank Transfer')),
    )

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        related_name="merchant",
        help_text=_("The user for whom account belongs to")
    )

    payment_ref = models.CharField(
        verbose_name = _("Payment Ref No"),
        max_length = 150,
        null=True,
        help_text=_("The payment ref number is an auto generated number from kroon kiosk to store each process by the merchant user be it cash, kroon token and card.")
    )

    payment_method = models.CharField(
        choices= PAYMENT_METHOD,
        verbose_name = _("Payment Method"),
        default = "card payment",
        max_length = 150,
        null=True,blank=True,
        help_text=_("The payment method used while paying for an order.")
    )

    amount_paid = models.DecimalField(
        verbose_name = _("Amount Paid"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_(" amount paid taken by the customer.")
    )

    cash_collected = models.DecimalField(
        verbose_name = _("Total Cash Amount Collect"),
        null=True, blank=True, 
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("toal amount taken for the cart.")
    )

    customers_change = models.DecimalField(
        verbose_name = _("Total Customers Change"),
        null=True,blank=True, 
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("toal amount taken for the cart.")
    )

    worker = models.CharField(
        verbose_name = _("Worker Name"), 
        max_length = 250,
        null=True,blank=True,
        help_text=_("this store the workers name that checkout the products for the particular store")
    )

    verified = models.BooleanField(
        verbose_name = _("Payment Verification"),
        default = False,
        null=True,blank=True,
        help_text=_("Verified payment status to identify if the payment is been verified by the payment gateway or not.")
    )

    status = models.CharField(
        verbose_name = _("Payment Status"),
        max_length = 150,
        null=True,
        help_text=_("payment status to identify if the payment is been verified by the payment gateway or not.")
    )


    def __str__(self):
        return str(self.payment_ref)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Kiosk Payment Record")
        verbose_name_plural = _("Kiosk Payment Record")


class Cart (BaseModel):
    cart_id = models.CharField(max_length=400, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem (BaseModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        help_text=_("The user for whom account belongs to")
    )
    
    worker = models.CharField(
        verbose_name = _("Worker"), 
        max_length = 250,
        null=True,blank=True,
        help_text=_("this store the workers name that checkout the products for the particular store")
    )

    product = models.ForeignKey(Merchant_Product, on_delete=models.CASCADE, null=True)
    product_variation = models.ManyToManyField(ProductVariation,  blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    weight_quantity = models.DecimalField(
        verbose_name = _("Weight Quantity"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,blank=True,
        help_text=_("the stores the product quantity via weight")
    )

    

    is_active = models.BooleanField(default=True, null=True)

    def sub_totals(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Merchant Cart")
        verbose_name_plural = _("Merchant Cart")



class Order (BaseModel):
    """
    Order model which is consist of the customer order details 
    and payment status information.
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        help_text=_("The user for whom account belongs to")
    )

    payment = models.ForeignKey(
        Payment, on_delete = models.CASCADE,
        null=True,blank=True,
        help_text=_("Customers order payment information.")
    )

    order_number = models.CharField(
        verbose_name = _("Order Number"),
        max_length = 150,
        null=True,
        help_text=_("Order generated number to identify the current customer order")
    )

    order_total = models.DecimalField(
        verbose_name = _("Total Amount"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("toal amount taken for the cart.")
    )

    products = models.ManyToManyField(
        Merchant_Product,
        verbose_name = _("Ordered Products"),
        blank=True,
        help_text=_("the list of ordered products for this particular checkout order")
    )

    refund = models.BooleanField(
        verbose_name = _("Order Refund"),
        default=False,
        null=True,blank=True,
        help_text= _("this indicates if the actual order is been refunded or not.")
    )

    worker = models.CharField(
        verbose_name = _("Worker"), 
        max_length = 250,
        null=True,blank=True,
        help_text=_("this store the workers name that checkout the products for the particular store")
    )

    is_ordered = models.BooleanField(
        verbose_name = _("Order Operation"),
        default=False,null=True,blank=True,
        help_text= _("the current state of the order , which identifies if the order is been processed successfully or not.")
    )

    def __str__(self):
        return str(self.user)


    class Meta:

        ordering = ('-created_date',)
        verbose_name = _("Kiosk Completed Order")
        verbose_name_plural = _("Kiosk Completed Order")


class OrderProduct (BaseModel):

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        help_text=_("The user for whom account belongs to")
    )

    worker = models.CharField(
        verbose_name = _("Worker Name"), 
        max_length = 250,
        null=True,blank=True,
        help_text=_("this store the workers name that checkout the products for the particular store")
    )

    order = models.ForeignKey(
        Order, on_delete = models.CASCADE,
        null=True, blank=True,
        help_text= _("foreign key and session to the order table.")
        )

    payment = models.ForeignKey(
        Payment, on_delete = models.CASCADE,
        null=True, blank=True,
        help_text= _("foreign key and session to the payment table.")
        )

    product = models.ForeignKey(
        Merchant_Product, on_delete = models.CASCADE,
        null=True, blank=True,
        help_text= _("foreign key and session to the product table.")
        )

    variation = models.ManyToManyField(
        ProductVariation, 
        blank=True,
        help_text= _("foreign key and session to the product variation table.")
        )
    
    # The ordered product quantity and price 

    quantity = models.IntegerField(
        verbose_name = _("Product Quantity"),
        null = True, blank=True,
        default = 0,
        help_text= _("product quantity for the current product been order by the customer.")
    )

    weight_quantity = models.DecimalField(
        verbose_name = _("Weight Quantity"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,blank=True,
        help_text=_("the stores the product quantity via weight")
    )

    product_price = models.DecimalField(
        verbose_name = _("Product Price "),
        null=True,blank=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("price for the current product.")
    )

    # the ordered product that is refunded

    refund_quantity = models.IntegerField(
        verbose_name = _("Refund Product Quantity"),
        null = True, blank=True,
        default = 0,
        help_text= _(" Refund product quantity for the current product been order by the customer.")
    )

    refund_weight_quantity = models.DecimalField(
        verbose_name = _(" Refund Weight Quantity"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,blank=True,
        help_text=_("the stores the Refund product quantity via weight")
    )

    refund_product_price = models.DecimalField(
        verbose_name = _("Refund Product Price "),
        null=True,blank=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("price for the current Refund product.")
    )


    product_total_price = models.DecimalField(
        verbose_name = _("Product Total Price "),
        null=True,blank=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,
        help_text=_("total price for the current product which is calculated by the quantity of the product with the product price.")
    )

    refund = models.BooleanField(
        verbose_name = _("Product Refund"),
        default=False,
        null=True,blank=True,
        help_text= _("this indicates if the actual product is been refunded or not.")
    )

    ordered = models.BooleanField(
        verbose_name = _("Order Operation"),
        default=False,null=True,blank=True,
        help_text= _("the current state of the order , which identifies if the order is been processed successfully or not.")
    )

    
    def __str__(self):
        return str(self.user)

    class Meta:

        ordering = ('-created_date',)
        verbose_name = _("Kiosk Ordered Products")
        verbose_name_plural = _("Kiosk Ordered Products")



