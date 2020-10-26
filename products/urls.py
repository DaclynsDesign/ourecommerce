from django.conf.urls import url

#Components / Apps views import
from .views import ProductList, ProductDetail #,FeaturedProduct,FeaturedProductDetail

urlpatterns = [
    url(r'^$', ProductList.as_view(), name='lists'),
    # url(r'^featured$', FeaturedProduct.as_view(), name='featured'),
    # url(r'^featured/(?P<pk>\d+)$', FeaturedProductDetail.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)$', ProductDetail.as_view(), name='detail')
] 
