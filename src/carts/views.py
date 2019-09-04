from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from .models import Cart
from billing.models import BillingProfile
from products.models import Product
from django.shortcuts import get_object_or_404
from orders.models import Order
from accounts.forms import LoginForm,RegisterForm
from addresses.models import Address
from addresses.forms import AddressForm
from django.http import JsonResponse
from django.views.generic import ListView,DetailView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
# from payments import get_payment_model, RedirectNeeded
# from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt


def cart_home(request):
	cart_obj, new_obj=Cart.objects.get_or_create(user=request.user,active=True)
	return render(request, "carts/home.html", {"cart":cart_obj})

def cart_add(request):
	product_id=request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Product Not Found")
			return redirect("carts:home")
		cart_obj, new_obj = Cart.objects.get_or_create(user=request.user,active=True)
		
		cart_obj.products.add(product_obj)
		added=True
		request.session['cart_items'] = cart_obj.products.count()
		
	return redirect("carts:home")
def cart_remove(request):
	product_id=request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Product Not Found")
			return redirect("carts:home")
		cart_obj, new_obj = Cart.objects.get_or_create(user=request.user,active=True)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			added=False
		request.session['cart_items'] = cart_obj.products.count()
	return redirect("carts:home")
def checkout_home(request):
	cart_obj, cart_created = Cart.objects.get_or_create(user=request.user, active=True)
	order_obj = None
	if cart_created or cart_obj.products.count() == 0:
		return redirect("carts:home")

	login_form = LoginForm()
	address_form = AddressForm()
	shipping_address_id = request.session.get("shipping_address_id", None)
	
	address_qs = None
	if request.user.is_authenticated:
		address_qs = Address.objects.filter(user=request.user)
	order_obj, order_obj_created = Order.objects.get_or_create(active=True,user=request.user, status='Created',cart=cart_obj)
	if shipping_address_id:
		order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
		del request.session["shipping_address_id"]
		order_obj.save()
		
	context = {
        "object": order_obj,
        "login_form": login_form, 
        "address_form": address_form,
        "address_qs": address_qs,}

	return render(request, "carts/checkout.html", context)
def checkout_done_view(request):
	Orders = Order.objects.filter(user=request.user)
	return render(request, "carts/checkout-done.html",{"orders":Orders})


class OrderDetail(DetailView):
	model = Order
	template_name="carts/order_detail.html"


class OrderDelete(UserPassesTestMixin,DeleteView):
	model = Order
	success_url = '/'
	def test_func(self):
		order= self.get_object()
		if self.request.user == order.user:
			return True
		return False

def pay(request):
	return render(request, 'carts/pay.html')


