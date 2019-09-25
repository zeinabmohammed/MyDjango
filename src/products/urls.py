
from django.urls import path,include

from products.views import (
				ProductListView,
				ProductDetailslugView,
				ProductMenView,
				ProductWomenView
				)
app_name= "products"
urlpatterns = [
	path('', ProductListView.as_view(), name="list"),
	path('<slug>', ProductDetailslugView.as_view(), name="detail"),
	path('men/',ProductMenView.as_view(),name='men'),
	path('women/',ProductWomenView.as_view(),name='women')
	#url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
	

	#url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
	#url(r'^featured/$', ProductFeaturedListView.as_view()),
	#url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),

	
	#url(r'^products-fbv/$', product_list_view),
	
]