from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
# Create your views here.
from .models import Product
from django.core.paginator import Paginator

from django.http import Http404 
from carts.models import Cart
class ProductFeaturedListView(ListView):
	
	template_name = "products/list.html"
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.featured()

class ProductMenView(ListView):
	queryset = Product.objects.filter(gender='men')
	template_name = "products/snippets/men.html"
class ProductWomenView(ListView):
	queryset = Product.objects.filter(gender='women')
	template_name = "products/snippets/women.html"	
	 # Show 25 contacts per page

	# def get_queryset(self, *args, **kwargs):
	# 	request = self.request
	# 	return Product.objects.featured()
class ProductListView(ListView):
	queryset = Product.objects.all()
	template_name = "products/list.html"
	paginate_by=6
	# # def get_context_data(self, *args, **kwargs):
	# 	context = super(ProductListView,self).get_context_data(*args, **kwargs)
	# 	print (context)
	# 	return context

# def product_list_view(request):
# 	queryset = Product.objects.all()
# 	context = {
# 		'object_list': queryset
# 	}
# 	return render(request, 'products/list.html', context)

class ProductDetailslugView(DetailView):
	queryset = Product.objects.all()

	template_name = "products/detail.html"
	def get_context_data(self, *args, **kwargs):
		context=super(ProductDetailslugView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart']= cart_obj
		return context
class ProductDetailView(DetailView):
	
	#queryset = Product.objects.all()#make aqueryset
	template_name = "products/detail.html"

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
	# 	print (context)
	# 	return context
	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product Not Here!")
		return instance
def product_detail_view(request, pk=None):
	#instance  = Product.objects.get(pk=pk)#id
	#instance = get_object_or_404(Product, pk=pk)
	# try:
	# 	instance=Product.objects.get(id=pk)
	# except Product.DoesNotExist:
	# 	print("No products here")
	# 	raise Http404("product not exist")
	# except:
	# 	print("huh?")
	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product Not Here!")
	#print (instance)
	# qs = Product.objects.filter(id=pk)
	# if qs.exists() and qs.count()==1:#count() returns the number of occurrences of a substring in the given string
	#determine the number of records in the set
	# 	instance = qs.first() #Return the first true value of an iterable
	# else:
	# 	raise Http404("Product Not Here!")
	context = {
		'object': instance
	}
	return render(request, 'products/detail.html', context)