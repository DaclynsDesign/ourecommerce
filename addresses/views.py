from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from .forms import AddressForm
from billings.models import BillingModel

# Create your views here.
def checkout_address_create(request):
    form = AddressForm(request.POST or None)
    context ={
        'form':form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    '''
    Saving shipping address to billing profile so that
    we can associate billing profile to shipping and save in database
    '''
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingModel.objects.new_or_get(request)
        
        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.save()

            request.session['shipping_address_id'] = instance.id
            shipping_address_id  = request.session.get('shipping_address_id',None)

        else:
            return redirect('cart:checkout')

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect('cart:checkout')
