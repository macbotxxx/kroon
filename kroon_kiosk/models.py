# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from helpers.common.basemodel import BaseModel
# from transactions.payment_gateway import PayStack
# from config.utils import unique_slug_generator_category, unique_slug_generator
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver

# from kroon.users.models import User
# from PIL import Image




# class Category (BaseModel):
#     """
#     kroon kiosk merchant category model, which gives the merchant permission to create, update and delete categories
#     """
#     user = models.ForeignKey(
#         User,
#         verbose_name=_("User Profile"),
#         on_delete=models.CASCADE, null=True,
#         help_text=_("The user for whom account belongs to")
#     )

#     category = models.CharField(
#         verbose_name=_("Category"),
#         max_length=255,
#         null=True,
#         help_text=_("this hold the category for the products the marchant will be uploading under this category")
#     )

#     slug = models.SlugField(
#         verbose_name = _('Category Slug'),
#         null=True,
#         max_length=300, blank=True,
#         help_text= _('Slug field for the category which is auto generated when the category is been created')
#         )

#     active = models.BooleanField(
#         verbose_name = _('Active'),
#         default=True, null=True,
#         help_text= _('this indicates whether the category is active or not')
#         )

#     class Meta:
#         verbose_name = _('Add or Delete Category')
#         verbose_name_plural = _('Add or Delete Category')

#     def __str__(self):
#         return str(self.category)

# def slug_generator_category(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator_category(instance)
# pre_save.connect(slug_generator_category, sender=Category)

    

# class Product (BaseModel):
#     """ Product model"""

#     user = models.ForeignKey(
#         User,
#         verbose_name=_("User Profile"),
#         on_delete=models.CASCADE, null=True,
#         help_text=_("The user for whom account belongs to")
#     )

#     product_sku = models.CharField(
#         verbose_name=_('Product SKU'),
#         max_length=500,
#         null=True,
#         help_text=_('Product sku should be added which identify each product')
#     )

#     product_name = models.CharField(
#         verbose_name=_('Product Name'),
#         max_length=500,
#         null=True,
#         help_text=_('Product name should be added which identify each product')
#     )

#     slug = models.SlugField(
#         verbose_name = _('Product Slug'),
#         null=True,
#         max_length=300, blank=True,
#         help_text= _('Slug field for the category which is auto generated when the product name is been created')
#     )

#     category = models.ForeignKey(
#         Category, on_delete = models.CASCADE,
#         verbose_name = _("Product category"),
#         null =True,
#         help_text= _('Product category will refrence the product category table which when the category is been deleted the items related to the parent or child category will be deleted as well.')

#     )

#     price = models.IntegerField (
#         verbose_name = _('Product Price'),
#         null =True,
#         help_text= _('Product price for the current product')
#     )

#     image = models.ImageField(
#         verbose_name = _('Product Image'),
#         upload_to = "photos/products",
#         null =True, 
#         help_text= _('Product image for the current product, which should be with no logo or trademark')
#     )

#     stock = models.IntegerField(
#         verbose_name = _('Total Stock'),
#         null=True,
#         help_text= _('Total Product availablity for the current item , which will automatically be tagged as out of stock when it reduces to zero.')
#     )

#     is_available = models.BooleanField(
#         verbose_name = _('Product availablity'),
#         default=True,
#         null=True,
#         help_text= _('Product availablity for this is item is been activated to false when the stock is less than 1 or activated to true when the stcok is greater than one')
#     )


    
#     class Meta:
#         ordering = ('-created_date',)
#         verbose_name = _("Merchant Product")
#         verbose_name_plural = _("Merchant Products")

#     @property
#     def category_name(self):
#         return self.category.category

#     def __str__(self):
#         return str(self.product_name)

#     #  to resize an image to a given height and width,
#     def save(self, *args, **kwargs):
#         if self.image:
#             super().save(*args, **kwargs)
#             # Image.open() can also open other image types
#             img = Image.open(self.image.path)
#             # WIDTH and HEIGHT are integers
#             resized_img = img.resize((640, 640))
#             resized_img.save(self.image.path)

# # product slug 
# def slug_generator(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
# pre_save.connect(slug_generator, sender=Product)





# class Cart (BaseModel):
#     cart_id = models.CharField(max_length=400, blank=True, null=True)
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.cart_id


# class CartItem (BaseModel):
#     user = models.ForeignKey(
#         User,
#         verbose_name=_("User Profile"),
#         on_delete=models.CASCADE, null=True,
#         help_text=_("The user for whom account belongs to")
#     )
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
#     quantity = models.IntegerField(null=True)
#     is_active = models.BooleanField(default=True, null=True)

#     def sub_totals(self):
#         return self.product.price * self.quantity

#     def __str__(self):
#         return str(self.user)

#     class Meta:
#         ordering = ('-created_date',)
#         verbose_name = _("Merchant Cart")
#         verbose_name_plural = _("Merchant Cart")



# class Payment(BaseModel):
#     """
#     Payement model for accepting orders.
#     """
#     PAYMENT_METHOD = (
#         ('kroon token', _('Kroon Token')),
#         ('card payment', _('Card Payment')),
#         ('cash payment', _('Cash Payment')),
#     )

#     user = models.ForeignKey(
#         User,
#         verbose_name=_("User Profile"),
#         on_delete=models.CASCADE, null=True,
#         related_name="merchant",
#         help_text=_("The user for whom account belongs to")
#     )

#     payment_ref = models.CharField(
#         verbose_name = _("Payment Ref No"),
#         max_length = 150,
#         null=True,
#         help_text=_("The payment ref number is an auto generated number from kroon kiosk to store each process by the merchant user be it cash, kroon token and card.")
#     )

#     payment_method = models.CharField(
#         choices= PAYMENT_METHOD,
#         verbose_name = _("Payment Method"),
#         default = "card payment",
#         max_length = 150,
#         null=True,blank=True,
#         help_text=_("The payment method used while paying for an order.")
#     )

#     amount_paid = models.IntegerField(
#         verbose_name = _("Amount Paid"),
#         null=True,
#         help_text=_("Amount paid for the above order by the customer.")
#     )

#     verified = models.BooleanField(
#         verbose_name = _("Payment Verification"),
#         default = False,
#         null=True,blank=True,
#         help_text=_("Verified payment status to identify if the payment is been verified by the payment gateway or not.")
#     )

#     status = models.CharField(
#         verbose_name = _("Payment Status"),
#         max_length = 150,
#         null=True,
#         help_text=_("payment status to identify if the payment is been verified by the payment gateway or not.")
#     )


#     def __str__(self):
#         return str(self.payment_ref)

#     class Meta:
#         ordering = ('-created_date',)
#         verbose_name = _("Kiosk Payment Record")
#         verbose_name_plural = _("Kiosk Payment Record")



# class Order (BaseModel):
#     """
#     Order model which is consist of the customer order details 
#     and payment status information.
#     """

#     user = models.ForeignKey(
#         User,
#         verbose_name=_("User Profile"),
#         on_delete=models.CASCADE, null=True,
#         help_text=_("The user for whom account belongs to")
#     )

#     payment = models.ForeignKey(
#         Payment, on_delete = models.CASCADE,
#         null=True,blank=True,
#         help_text=_("Customers order payment information.")
#     )

#     order_number = models.CharField(
#         verbose_name = _("Order Number"),
#         max_length = 150,
#         null=True,
#         help_text=_("Order generated number to identify the current customer order")
#     )

#     order_total = models.IntegerField(
#         verbose_name = _("Order Total Amount"),
#         null=True,blank=True,
#         help_text=_("Total amount for the current order placed by the customer")
#     )

#     is_ordered = models.BooleanField(
#         verbose_name = _("Order Operation"),
#         default=False,null=True,blank=True,
#         help_text= _("the current state of the order , which identifies if the order is been processed successfully or not.")
#     )

#     def __str__(self):
#         return str(self.user)


#     class Meta:

#         ordering = ('-created_date',)
#         verbose_name = _("Kiosk Completed Order")
#         verbose_name_plural = _("Kiosk Completed Order")


# class OrderProduct (BaseModel):

#     user = models.ForeignKey(
#         User,
#         verbose_name=_("User Profile"),
#         on_delete=models.CASCADE, null=True,
#         help_text=_("The user for whom account belongs to")
#     )

#     order = models.ForeignKey(
#         Order, on_delete = models.CASCADE,
#         null=True, blank=True,
#         help_text= _("foreign key and session to the order table.")
#         )

#     payment = models.ForeignKey(
#         Payment, on_delete = models.CASCADE,
#         null=True, blank=True,
#         help_text= _("foreign key and session to the payment table.")
#         )

#     product = models.ForeignKey(
#         Product, on_delete = models.CASCADE,
#         null=True, blank=True,
#         help_text= _("foreign key and session to the product table.")
#         )

#     quantity = models.IntegerField(
#         verbose_name = _("Product Quantity"),
#         null = True, blank=True,
#         help_text= _("product quantity for the current product been order by the customer.")
#     )

#     ordered = models.BooleanField(
#         verbose_name = _("Order Operation"),
#         default=False,null=True,blank=True,
#         help_text= _("the current state of the order , which identifies if the order is been processed successfully or not.")
#     )

    
#     def __str__(self):
#         return str(self.user)

#     class Meta:

#         ordering = ('-created_date',)
#         verbose_name = _("Kiosk Ordered Products")
#         verbose_name_plural = _("Kiosk Ordered Products")
    
    

