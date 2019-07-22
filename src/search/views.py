from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
# from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


class SearchProductView(ListView):
	model = Product
	template_name = "search/view.html"
	def get_queryset(self, *args, **kwargs):
		qs = Product.objects.all()
		keywords = self.request.GET.get('q', None)
		if keywords is not None:
			qs = qs.filter(
						Q(title__icontains=keywords)|
						Q(description__icontains=keywords)|
						Q(tag__title__icontains=keywords)|
						Q(slug__icontains=keywords)).distinct()
		return qs

		# if keywords is not None:
		# 	lookups=(
		# 				Q(title__icontains=keywords),
		# 				Q(description__icontains=keywords),
		# 				Q(slug__icontains=keywords))
		# 	return Product.objects.filter(lookups).distinct()
		# return qs

"""distinct() remove duplicated values"""