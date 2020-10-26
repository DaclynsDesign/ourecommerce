from django.shortcuts import render, redirect
from django.http import JsonResponse #used to handle JSON Request
from products.models import ProductModel
from orders.models import OrderModel
from .models import CartModel
from billings.models import BillingModel
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmailModel
from addresses.forms import AddressForm
from addresses.models import Address



def cart_refresh(request):
    cart_obj, new_obj = CartModel.objects.new_or_get_cart(request)
    products =[
        {
            'id':x.id,
            'name':x.title,
            'price':x.price,
            'url': x.get_absolute_url(),
            'image':x.image.url
        
        } 
        for x in cart_obj.products.all()]
    cart_data = {'products':products,'subtotal':cart_obj.subtotal, 'total':cart_obj.total}
    return JsonResponse(cart_data)

# The view function for displaying our cart home where products have been added
#Creating a new cart
def cart_home(request):
    cart_obj, new_obj = CartModel.objects.new_or_get_cart(request)
    return render(request, 'carts/home.html',{'cart':cart_obj})


# Code for updating cart when product is added or removed
def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = ProductModel.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('cart:home')
        cart_obj, new_obj = CartModel.objects.new_or_get_cart(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            product_added = False
        else:
            cart_obj.products.add(product_obj)
            product_added = True
        request.session['cart_items'] = cart_obj.products.count()
    # return redirect(product_obj.get_absolute_url())
        if request.is_ajax():
        #Letting django handle json request from frontend jquery
        #done by import JsonResponse from django.htp
            json_data={
                "added":product_added,
                'removed': not product_added,
                'cartItemcount': cart_obj.products.count(),
            }
            return JsonResponse(json_data)
    return redirect('cart:home')


# Check out view 
def checkout_home(request):
    cart_obj, cart_created = CartModel.objects.new_or_get_cart(request)
    order_obj = None
    if cart_created or cart_obj.products.count() ==0:
        return redirect("cart:home")
    #Login form
    login_form = LoginForm()
    #Guest form
    guest_form = GuestForm()
    #Address Form
    address_form = AddressForm()
    
    shipping_address_id  = request.session.get('shipping_address_id',None)

    billing_profile, billing_profile_created = BillingModel.objects.new_or_get(request)

    if billing_profile is not None:
        order_obj, order_obj_created = OrderModel.objects.new_or_get(billing_profile,cart_obj)

        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
            order_obj.save()

    if request.method == 'POST':
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect('cart:success')


    context = {
        'object':order_obj,
        'billing_profile': billing_profile,
        'login_form':login_form,
        'guest_form':guest_form,
        'address_form':address_form
    }
    
    return render(request,'carts/checkout.html',context)




#Checkout Complete view
def checkout_done(request):
   return render(request,'carts/success.html',{})



