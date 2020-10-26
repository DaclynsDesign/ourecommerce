from math import fsum
from django.db import models
from django.db.models.signals import pre_save,post_save
from carts.models import CartModel
from billings.models import BillingModel
from tiptoe.utils import unique_order_id_generator
from addresses.models import Address

# Create your models here.
ORDER_STATUS = (
    ("created",'Created'),
    ('paid','Paid'),
    ("shipped",'Shipped'),
    ('Returned','Returned')
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count()==1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile = billing_profile, cart=cart_obj)
            created = True
        return obj, created


class OrderModel(models.Model):
    order_id = models.CharField(max_length=30, blank=True)
    billing_profile = models.ForeignKey(BillingModel, null=True, blank=True)
    shipping_address = models.ForeignKey(Address, null=True, blank=True)
    cart = models.ForeignKey(CartModel)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default='created')
    delivery_total = models.DecimalField(decimal_places=2, max_digits=20, default=10.00)
    total = models.DecimalField(decimal_places=2, max_digits=20, default=10.00)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.order_id

    objects = OrderManager()

    #calculations and updating total 
    def update_total(self):
        cart_total = self.cart.total
        delivery_total = self.delivery_total
        new_total = fsum([cart_total ,delivery_total])
        self.total = new_total
        self.save()
        return new_total

    #Checking if our Order is done or completed
    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        total = self.total
        if billing_profile and shipping_address and total > 0:
            return True
        return False 

    #Making order as paid
    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
        return self.status    





def order_id_pre_save_receiver(sender, instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = OrderModel.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(order_id_pre_save_receiver, sender=OrderModel)


# Updating order total when cart changes
def post_save_cart_total(sender, instance,created,*args,**kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = OrderModel.objects.filter(cart__id = cart_id)
        if qs.count() ==1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total,sender=CartModel)

def post_save_order(sender, instance, created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order,sender=OrderModel)