from django.views.generic import ListView
from products.models import ProductModel

class Home(ListView):
    queryset=ProductModel.objects.all()
    template_name='home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['adinkra_list'] = ProductModel.objects.adinkra()
        context['couple_list'] = ProductModel.objects.couple()
        context['facial_list'] = ProductModel.objects.facial()
        context['fashion_list'] = ProductModel.objects.fashion()
        # And so on for more models
        return context