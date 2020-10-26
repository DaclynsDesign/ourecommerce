from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ProductModel
from carts.models import CartModel
'''
    NB: Every class based view takes in a model which gives us 
    context and it automatically use get_context_data 
    method to pull it out to our template
'''
# Create your views here.


class ProductList(ListView):
    # queryset = ProductModel.objects.all()
    model = ProductModel
    template_name = 'product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        cart_obj, new_obj = CartModel.objects.new_or_get_cart(self.request)
        context['cart'] = cart_obj
        return context



class ProductDetail(DetailView):
    model = ProductModel
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        cart_obj, new_obj = CartModel.objects.new_or_get_cart(self.request)
        context['cart'] = cart_obj
        return context
        

'''
The below code lets us implement featured products
so we can see products that are featured
'''
# class FeaturedProduct(ListView):
#     queryset = ProductModel.objects.featured()
#     template_name = 'product_list.html'


# class FeaturedProductDetail(DetailView):
#     queryset = ProductModel.objects.featured()
#     template_name = 'product_detail.html'
 