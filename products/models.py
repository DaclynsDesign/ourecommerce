import random
import os

from django.db import models
from django.db.models import Q #for search functionality
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from tiptoe.utils import unique_slug_generator 


# function to handle fileupload whether from a path or source or image

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

# File upload path and rename

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 2019999)
    name, ext = get_filename_ext(filename)
    renamedfile = f'{new_filename}{ext}'
    return f'products/{new_filename}/{renamedfile}'

#Create your model Managers here
class ProductManager(models.Manager):
    #Featured product manager, lets us do Products.objects.featured
    def featured(self):
        return self.get_queryset().filter(featured=True)

    #Recommended product manager, lets us do Products.objects.recommended
    def recommended(self):
        return self.get_queryset().filter(recommended=True)
    

    # Our manager 
    def adinkra(self):
        return self.get_queryset().filter(adinkra=True)

    def couple(self):
        return self.get_queryset().filter(couple=True)
    
    def facial(self):
        return self.get_queryset().filter(facial=True)

    def fashion(self):
        return self.get_queryset().filter(fashion=True)

    #Search
    def search(self, query):
        lookups = (Q(title__icontains=query)|
                    Q(description__icontains=query)|
                    Q(price__icontains=query)|
                    Q(tagmodel__title__icontains=query)
                )
        return self.get_queryset().filter(lookups).distinct() 

# Create your models here.

class ProductModel(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    image  = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    
    # Our boolean
    adinkra = models.BooleanField(default=False)
    couple = models.BooleanField(default=False)
    facial = models.BooleanField(default=False)
    fashion = models.BooleanField(default=False)


    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

#signals to save unique slug name to admin
def product_pre_save_receiver(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver,sender=ProductModel)