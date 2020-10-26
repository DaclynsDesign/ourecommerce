from django.db import models
from django.db.models.signals import pre_save, post_save
from tiptoe.utils import unique_slug_generator 
from products.models import ProductModel

# Create your models here.
class TagModel(models.Model):
    products = models.ManyToManyField(ProductModel, blank=True)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#signals to save unique slug name to admin
def tag_pre_save_receiver(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver,sender=TagModel)