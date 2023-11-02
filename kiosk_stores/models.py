from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from config.utils import unique_name_generator_product_name, unique_slug_generator, unique_product_sku_generator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from django.template import Context


from kiosk_categories.models import Category 
from kroon.users.models import User, BusinessProfile
from PIL import Image



class Merchant_Product(BaseModel):
    """ Product model"""

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.CASCADE, null=True,
        related_name="merchant_products",
        blank=True,
        help_text=_("The user for whom account belongs to")
    )

    business_profile = models.ForeignKey(
        BusinessProfile,
        verbose_name=_("Business Profile"),
        on_delete=models.CASCADE, null=True,
        related_name="business_accounts",
        blank=True,
        help_text=_("This is the business profile associated with the product")
    )

    product_sku = models.CharField(
        verbose_name=_('Product SKU'),
        max_length=500,
        null=True,blank=True,
        help_text=_('Product sku should be added which identify each product')
    )

    product_name = models.CharField(
        verbose_name=_('Product Name'),
        max_length=500,
        null=True,
        help_text=_('Product name should be added which identify each product')
    )

    slug = models.SlugField(
        verbose_name = _('Product Slug'),
        null=True,
        max_length=300, blank=True,
        help_text= _('Slug field for the category which is auto generated when the product name is been created')
    )

    category = models.ForeignKey(
        Category, on_delete = models.CASCADE,
        verbose_name = _("Product category"),
        null =True,blank=True,
        help_text= _('Product category will refrence the product category table which when the category is been deleted the items related to the parent or child category will be deleted as well.')

    )

    price = models.DecimalField(
        verbose_name = _("Amount In Local Currency"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,blank=True,
        help_text=_("the product amount which will be store in local currency")
    )

    cost_price = models.DecimalField(
        verbose_name = _("Cost Amount In Local Currency"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,blank=True,
        help_text=_("the product cost amount which will be store in local currency")
    )

    merchant_local_currency = models.CharField(
        verbose_name=_('Merchant Local Currency'),
        max_length=50,
        null=True,blank=True,
        help_text=_('Merchant local currency is been saved for the current product')
    )

    image = models.ImageField(
        verbose_name = _('Product Image'),
        upload_to = "photos/products",
        null = True,blank=True,
        help_text= _('Product image for the current product, which should be with no logo or trademark')
    )

    stock = models.IntegerField(
        verbose_name = _('Total Stock'),
        null=True,blank=True,
        default = 0,
        help_text= _('Total Product availablity for the current item , which will automatically be tagged as out of stock when it reduces to zero.')
    )

    charge_by_weight = models.BooleanField(
        verbose_name = _('Charge By Weight'),
        default=True,
        null=True,blank=True,
        help_text= _('if this action is been ticked the product sale price will be used to calculate the product if only the customer is buying it by size which includes weight or kilogram.')
    )

    weight_quantity = models.DecimalField(
        verbose_name = _("Weight Quantity"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,blank=True,
        help_text=_("the stores the product quantity via weight")
    )

    weight_unit = models.CharField(
        verbose_name=_('Weight Unit'),
        max_length=50,
        default= "KG",
        null=True,blank=True,
        help_text=_('product weight unit is meant to be inputed by the merchant or the product uploader.')
    )

    out_of_stock_notify = models.BooleanField(
        verbose_name = _('Out Of Stock Notify'),
        default=False,
        null=True,blank=True,
        help_text= _('the true or false button identifies to the customer is he or she want to be notified when the stock is below the a given number ')
    )
    
    low_stock_limit = models.CharField(
        verbose_name=_('Low Stock Limit'),
        max_length=50,
        null=True,blank=True,
        help_text=_('this input store the stock limitation by which the merchant gets notified about his or low sotck level')
    )

    expire_notify = models.BooleanField(
        verbose_name = _('Expire Notification'),
        default=False,
        null=True,blank=True,
        help_text= _('this indicates if the expiration notification will be sent to the merchant ')
    )
    
    expiring_date = models.DateField(
        verbose_name=_('Expiring Date'),
        max_length=50,
        null=True,
        blank=True,
        help_text=_('this storess the product expiring date and from which the merchant will be notified')
    )

    expiry_days_notify = models.IntegerField(
        verbose_name = _('Expiry Days'),
        null=True,blank=True,
        default = 0,
        help_text= _('This shows the days before the expiring date for the merchant to get the push notifications')
    )

    is_available = models.BooleanField(
        verbose_name = _('Product availablity'),
        default=True,
        null=True,blank=True,
        help_text= _('Product availablity for this is item is been activated to false when the stock is less than 1 or activated to true when the stcok is greater than one')
    )

    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Merchant Product")
        verbose_name_plural = _("Merchant Products")

    @property
    def category_name(self):
        return self.category.category

    def __str__(self):
        return str(self.product_name)

    # to resize an image to a given height and width,
    # this action is meant to reduce the size of the image
    # def save(self, *args, **kwargs):
    #     if self.image:
    #         super().save(*args, **kwargs)
    #         # Image.open() can also open other image types
    #         img = Image.open(self.image.path)
    #         # WIDTH and HEIGHT are integers
    #         # if img.height > 800 or img.width > 800:
    #         resized_img = img.resize((150, 150))
    #         resized_img.save(self.image.path)
    #     else:
    #         pass

    # def save(self):
    #     user = super().save()
    #     image = Image.open(self.image)
    #     resized_image = image.resize((200, 200), Image.ANTIALIAS)
    #     fh = storage.open(self.image.name, "w")
    #     resized_image.save(fh)
    #     fh.close()
    #     # resized_image.save(self.image.path)
    #     return user



# product slug 
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(slug_generator, sender=Merchant_Product)

# making product unique to a user 
def product_name_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.product_name = unique_name_generator_product_name(instance)
pre_save.connect(product_name_generator, sender=Merchant_Product)

# this saves the product sku to be unique
def product_sku_generator(sender, instance, *args, **kwargs):
    if not instance.product_sku:
        instance.product_sku = unique_product_sku_generator(instance)
pre_save.connect(product_sku_generator, sender=Merchant_Product)


# product variation manager interface
class ProductVariationManager(models.Manager):
    # variation function for the color of the product
    def colors (self):
        return super(ProductVariationManager, self).filter(variations_category="Color", is_active = True)

    # variation function for thr product size
    def sizes (self):
        return super(ProductVariationManager, self).filter(variations_category="Size", is_active = True)


# product variation category list
VARIATION_CATEGORIES_LIST = (
    ('Color', 'Color'),
    ('Size', 'Size'),
)


class ProductVariation(BaseModel):
    """
    Product variations models for the current product function.
    """
    # registering custom manager interface
    objects = ProductVariationManager()

    product = models.ForeignKey(
        Merchant_Product, on_delete=models.CASCADE,
        null=True,
        related_name='products_variation',
        verbose_name = _('Product Name'),
        help_text = _('Product name refering to the product already uplaoded and to be added some variatons.')
    )

    variations_category = models.CharField(
        verbose_name = _('Variations'),
        max_length = 255,
        null=True,blank=True,
        choices=VARIATION_CATEGORIES_LIST,
        help_text = _("Select which variation category to the current product")
    )

    variation_value = models.CharField(
        verbose_name = _('Variation Value'),
        null =True,
        max_length = 250,blank=True,
        help_text=_("the value to select for the variation product")
    )

    quantity = models.IntegerField(
        verbose_name = _('Quantity'),
        null=True,
        blank=True,
        help_text=_("the value holds the quantity for the product variation which will be deducated when ever the product is been added to cart and will also have a status of low qunatity, when ever its been out of stock.")
    )

    weight_quantity = models.DecimalField(
        verbose_name = _("Weight Quantity"),
        null=True,
        max_digits = 300, decimal_places = 2,
        default=0.00,blank=True,
        help_text=_("the stores the product quantity via weight")
    )

    is_active = models.BooleanField(
        verbose_name=_("Variation Status"),
        default = True,
        null =True,blank=True,
        help_text=_("Status to dectect if the product variation is active or not")
    )
    

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Product Variation ")
        verbose_name_plural = _("Product Variation")

    def __str__(self):
        return str(self.variation_value)