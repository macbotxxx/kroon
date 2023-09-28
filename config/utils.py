import random
import string
from io import BytesIO

from django.utils.text import slugify
from django.http import HttpResponse
from django.template.loader import get_template

# from xhtml2pdf import pisa

#  creating slugs starts from here 

def random_string_generator(size=10,chars=string.ascii_lowercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
      if new_slug is not None:
            slug = new_slug
      else:
            slug = slugify(instance.product_name)

      klass = instance.__class__
      qs_exists = klass.objects.filter(slug=slug).exists()
      if qs_exists:
            new_slug="{slug}-{randstr}".format(
                  slug=slug,
                  randstr = random_string_generator(size=6)
            )
            return unique_slug_generator(instance,new_slug=new_slug)
      return slug

# giving a new unique product sku
def unique_product_sku_generator(instance, new_product_sku=None):
      if new_product_sku is not None:
            product_sku = new_product_sku
      else:
            product_sku = slugify(instance.product_sku)

      klass = instance.__class__
      qs_exists = klass.objects.filter(product_sku=product_sku).exists()
      if qs_exists:
            new_product_sku="{product_sku}-{randstr}".format(
                  product_sku=product_sku,
                  randstr = random_string_generator(size=6)
            )
            return unique_product_sku_generator(instance,new_product_sku=new_product_sku)
      return product_sku

 

def unique_slug_generator_category(instance, new_slug=None):
      if new_slug is not None:
            slug = new_slug
      else:
            slug = slugify(instance.category)

      klass = instance.__class__
      qs_exists = klass.objects.filter(slug=slug).exists()
      if qs_exists:
            new_slug="{slug}-{randstr}".format(
                  slug=slug,
                  randstr = random_string_generator(size=4)
            )
            return unique_slug_generator_category(instance,new_slug=new_slug)
      return slug



def unique_name_generator_product_name(instance, new_slug=None):
      if new_slug is not None:
            slug = new_slug
      else:
            slug = slugify(instance.product_name)

      klass = instance.__class__
      qs_exists = klass.objects.filter(slug=slug).exists()
      if qs_exists:
            new_slug="{slug}-{randstr}".format(
                  slug=slug,
                  randstr = random_string_generator(size=4)
            )
            return unique_name_generator_product_name(instance,new_slug=new_slug)
      return slug



# Wallet ID generator based on registered users

def random_string_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_wallet_id_generator(instance):
    order_new_id = random_string_generator()
    Klass= instance.__class__
    qs_exists= Klass.objects.filter(wallet_id= order_new_id).exists()
    if qs_exists:
        return unique_wallet_id_generator(instance)
    return order_new_id


# pdf handling function

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


    
