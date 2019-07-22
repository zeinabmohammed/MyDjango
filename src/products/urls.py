
from django.urls import path

from products.views import (
				ProductListView,
				ProductDetailslugView
				)
app_name= "products"
urlpatterns = [
	path('', ProductListView.as_view(), name="list"),
	path('<slug>', ProductDetailslugView.as_view(), name="detail"),
	#url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
	

	#url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
	#url(r'^featured/$', ProductFeaturedListView.as_view()),
	#url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),

	
	#url(r'^products-fbv/$', product_list_view),
	
]