
import math
from django.db import models
from carts.models import Cart
from django.db.models.signals import pre_save,post_save
from ecommerce.utils import unique_order_id_generator
from billing.models import BillingProfile
from addresses.models import Address

ORDER_STATUS_CHOISES=(
		('created', "Created"),
		('paid', "Paid"),
		('shipped', "Shipped"),
		('refunded', "Refunded"),

	)
class OrderManager(models.Manager):
	def new_or_get(self, billing_profile, cart_obj):
		qs = self.get_queryset().filter(billing_profile= billing_profile , cart=cart_obj, active=True)
		created=False

		if qs.count()==1:
			obj=qs.first()
		else:
			obj= Order.objects.create(cart=cart_obj, billing_profile=billing_profile)
			created=True
		return obj, created
	
class Order(models.Model):
	billing_profile  = models.ForeignKey(BillingProfile, on_delete='CASCADE', null=True)
	shipping_address = models.ForeignKey(Address, on_delete='CASCADE',related_name="shipping_address",null=True, blank=True)
	shipping_address_final    = models.TextField(blank=True, null=True)
	order_id 		 = models.CharField(max_length=120, blank=True)
	cart 			 = models.ForeignKey(Cart, on_delete=models.CASCADE)
	status 			 = models.CharField(max_length=120, default="created", choices=ORDER_STATUS_CHOISES)
	shipping_total   = models.DecimalField(default=5.00, max_digits=100, decimal_places=2)
	total 			 = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	active           = models.BooleanField(default=True)

	objects = OrderManager()

	def __str__(self):
		return self.order_id


	def update_total(self):
		cart_total = self.cart.total
		shipping_total = self.shipping_total
		new_total = math.fsum([cart_total , shipping_total])
		formatted_total=format(new_total,'2f')
		self.total = formatted_total
		self.save()
		return new_total
		
		def get_status(self):
	        if self.status == "refunded":
	            return "Refunded order"
	        elif self.status == "shipped":
	            return "Shipped"
	        return "Shipping Soon"


def pre_save_create_order_id(sender, instance, *args, **kwargs):
	if not instance.order_id:
		instance.order_id = unique_order_id_generator(instance)
	qs=Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)
	if instance.shipping_address and not instance.shipping_address_final:
		instance.shipping_address_final = instance.shipping_address.get_address()
pre_save.connect(pre_save_create_order_id, sender=Order)
def post_save_cart_total(sender, instance, created, *args, **kwargs):
	if not created:
		cart_obj   = instance
		cart_total = cart_obj.total
		cart_id    = cart_obj.id
		qs = Order.objects.filter(cart__id=cart_id)
		if qs.count()==1:
			order_obj = qs.first()
			order_obj.update_total()
post_save.connect(post_save_cart_total, sender=Cart)
def post_save_order(sender ,created, instance, *args, **kwargs):
	if created:
		instance.update_total()
post_save.connect(post_save_order, sender=Order)
