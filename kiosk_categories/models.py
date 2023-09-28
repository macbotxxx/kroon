from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from config.utils import unique_slug_generator_category
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from PIL import Image




class Category(MPTTModel):
    
    category = models.CharField(
        verbose_name = _('Category Name'),
        max_length=80, unique=True,
        null=True, 
        help_text = _('Specify the category name.')
        )

    parent = TreeForeignKey(
        'self',
        verbose_name = _('Category Parent'),
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        help_text=_('Parent category refers to the main parent of the child category')
        )
    slug = models.SlugField(
        verbose_name = _('Category Slug'),
        null=True,
        max_length=300, blank=True,
        help_text= _('Slug field for the category which is auto generated when the category is been created')
        )

    image = models.ImageField(
        upload_to = "categories_image/", 
        verbose_name = _('Category Image'),
        null=True,blank = True,
        help_text = _("category image is meant to be png JPG JPEG"),
        )
   
   
    def __str__(self):
        return self.category

        
    class MPTTMeta:
        order_insertion_by = ['category']
        

    class Meta:
        verbose_name = _('Add or Delete Category')
        verbose_name_plural = _('Add or Delete Category')


    def __str__(self):
        full_path = [self.category]
        k = self.parent
        while k is not None:
            full_path.append(k.category)
            k = k.parent
        return '/'.join(full_path[::-1])

       #  to resize an image to a given height and width,
    # def save(self, *args, **kwargs):
    #     if self.image:
    #         super().save(*args, **kwargs)
    #         # Image.open() can also open other image types
    #         img = Image.open(self.image.path)
    #         # WIDTH and HEIGHT are integers
    #         resized_img = img.resize((287, 427))
    #         resized_img.save(self.image.path)



def slug_generator_category(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_category(instance)


pre_save.connect(slug_generator_category, sender=Category)
