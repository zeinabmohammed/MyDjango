
from django.urls import path, include

from .views import (
				cart_home,
				cart_add,
				checkout_home,
				checkout_done_view,
				cart_remove,
				OrderDetail,
				OrderDelete,
				pay,
				)
app_name= "carts"
urlpatterns = [
	path('', cart_home, name="home"),
	path('update', cart_add, name="update"),
	path('remove', cart_remove, name="remove"),
	path('checkout', checkout_home, name="checkout"),
	path('checkout/done', checkout_done_view, name="checkout_done"),
	path('order/<pk>', OrderDetail.as_view(), name="OrderDetail"),
	path('order/<int:pk>/delete', OrderDelete.as_view(), name="OrderDelete"),
	path('paypal/', include('paypal.standard.ipn.urls')),
	path('pay/',pay,name='pay'),
	# path('guest_register', guest_register_view, name="guest_register"),
	# path('delete/<id>', removeproduct, name="remove"),
	]