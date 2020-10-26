"""tiptoe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#Url settings for static to work
from django.conf import settings
from django.conf.urls.static import static


from django.conf.urls import url, include
from django.contrib import admin

#My import for my own views
from .views import Home

#Login and Logout 
from accounts.views import LoginView,guest_register,RegisterView
from django.contrib.auth.views import LogoutView #,LoginView
from addresses.views import checkout_address_create
from carts.views import cart_refresh 


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^checkout/address/create/$',checkout_address_create,name='checkout_address_create'),
    url(r'^register/guest$', guest_register, name='guest_register'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^api/cart/$', cart_refresh, name='api-cart'),
    url(r'^cart/', include('carts.urls', namespace='cart')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^search/', include('search.urls', namespace='search')),

    url(r'^register/$', RegisterView.as_view(), name='register'),
] 
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


