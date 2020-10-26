from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save, m2m_changed

from products.models import ProductModel

User = settings.AUTH_USER_MODEL


#Cart Manager
class CartModelManager(models.Manager):
    def new_or_get_cart(self,request):
        '''
        In this method we are checking if a cart exists and if it does we print out
        cart_id exists but if cart doesnt exists, we use cart.objects.create to create
        a new one
        '''
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() ==1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = CartModel.objects.new_cart(user = request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    #Creating new cart
    def new_cart(self, user=None):
        '''
        During the session and cartid creation if user is authenticated
        then lets assign that user to that session and cart
        '''
        user_obj = None 
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


# Create your models here.
class CartModel(models.Model):
    user = models.ForeignKey(User, null=True , blank=True)
    products = models.ManyToManyField(ProductModel, blank=True)
    subtotal = models.DecimalField(decimal_places=0, max_digits=10, default=0.10)
    total = models.DecimalField(decimal_places=0, max_digits=10, default=0.10)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartModelManager()

    def __str__(self):
        return str(self.id) 



#Using signals to save product total and products change to calculate subtotal
#Ne signal introduced m2mchanged
def m2m_changed_cart_receiver(sender,instance, action,*args,**kwargs):
    if action == 'post_add' or action == 'post_remove' or action=='post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total 
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver,  sender=CartModel.products.through)

def pre_save_cart_receiver(sender, instance, *args,**kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal #+ 10
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver,sender=CartModel)