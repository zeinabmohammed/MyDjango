from django.db import models
import random
import os
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_slug_generator
from django.contrib.auth.models import User

class ProductQueryset(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)
	def get_by_id(self, id):
		qs = self.filter(id=id)
		if qs.count()== 1:
			return qs.first()
		else:
			return None	
	def featured(self):
		return self.filter(featured=True)
	def men(self):
		return self.filter(gender='men')
	# def all(self):
	# 	return self.filter(active=True)
# class  ProductManager(models.Manager):
# 	def get_queryset(self):
# 		return ProductQueryset(self.model, using=self._db)
# 	def featured(self):
# 		return self.get_queryset().filter(featured=True)
# 	def all(self):
# 		return self.get_queryset().active()
	
# 	def search(self, query):
# 		return self.get_queryset().active().search(query)

GENDER_CHOISES=(

		('men', "Men"),
		('women', "Women"),)
class Product(models.Model):
	title         = models.CharField(max_length=120)
	slug          = models.SlugField(blank=True, unique=True)
	description   = models.TextField()
	price         = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
	image         = models.ImageField(upload_to='products', null=True, blank=False)
	featured      = models.BooleanField(default=False)
	active        = models.BooleanField(default=True)
	gender 		  = models.CharField(max_length=120,default="" ,choices=GENDER_CHOISES)
	timestamp     = models.DateTimeField(auto_now_add=True)
	
	objects = ProductQueryset.as_manager()


	def get_absolute_url(self):
		#return "/products/{slug}/".format(slug=self.slug)
		return reverse("products:detail", kwargs={"slug":self.slug})

	def __str__(self):
		"""show product name in admin page"""
		return self.title


	def product_pre_save_receiver(sender, instance, *args, **kwargs):
		if not instance.slug:
			instance.slug = unique_slug_generator(instance)
		pre_save.connect(Product_pre_save_receiver, sender=Product)
