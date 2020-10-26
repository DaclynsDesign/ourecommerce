from django.conf.urls import url

#Components / Apps views import
from .views import SearchView

urlpatterns = [
    url(r'^$', SearchView.as_view(), name='query'),
] 
