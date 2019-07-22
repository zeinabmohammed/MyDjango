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
# from accounts.models import GuestEmail
# def cart_create(user=None):
# 	new_cart = Cart.objects.create(user=None)
# 	print ('New cart created')
# 	return new_cart
def cart_home(request):
	cart_obj, new_obj=Cart.objects.new_or_get(request)
	return render(request, "carts/home.html", {"cart":cart_obj})

def cart_add(request):
	product_id=request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Product Not Found")
			return redirect("cart:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		
		cart_obj.products.add(product_obj)
		added=True
		request.session['cart_items'] = cart_obj.products.count()
		# if request.is_ajax(): # Asynchronous JavaScript And XML / JSON
		# 	print("Ajax request")
		# 	json_data = {
		# 	"added": added,
		# 	"removed": not added,
		# 	"cartItemCount": cart_obj.products.count()}
		# 	return JsonResponse(json_data, status=200)
	return redirect("carts:home")
def cart_remove(request):
	product_id=request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Product Not Found")
			return redirect("cart:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			added=False
		request.session['cart_items'] = cart_obj.products.count()
	return redirect("carts:home")
def checkout_home(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	order_obj = None
	if cart_created or cart_obj.products.count() == 0:
		return redirect("cart:home")
	login_form = LoginForm()
	address_form = AddressForm()
	billing_address_id = request.session.get("billing_address_id", None)

    # shipping_address_required = not cart_obj.is_digital

	shipping_address_id = request.session.get("shipping_address_id", None)
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	address_qs = None
	if billing_profile is not None:
		if request.user.is_authenticated:
			address_qs = Address.objects.filter(billing_profile=billing_profile)
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del request.session["shipping_address_id"]
		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del request.session["billing_address_id"]
		if billing_address_id or shipping_address_id:
			order_obj.save()
	context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        
        "address_form": address_form,
        "address_qs": address_qs,}

	return render(request, "carts/checkout.html", context)

def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})