from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from products.models import ProductModel

# Create your views here.

class SearchView(ListView):
    template_name='searchview.html'
    queryset = ProductModel.objects.all()

    def get_queryset(self,*args,**kwargs):
        request = self.request 
        method_dict = request.GET 
        query = method_dict.get('q',None)
        if query is not None:
            return ProductModel.objects.search(query)
        return ProductModel.objects.featured()

    '''
    So the above code takes a look at the user request in the url and see if the
    request contains a query for search and it grabs it as display is as a dict type
    then we check if there is a search word like "Bags" we filter our products based
    on the query. Else we return either featured product or recommended product.
    '''