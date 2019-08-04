
from django.db import models
from billing.models import BillingProfile
from django.contrib.auth.models import User
class Address(models.Model):
	user            = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
	name            = models.CharField(max_length=120, null=True, blank=True, help_text='Shipping to? Who is it for?')
	address_line_1  = models.CharField(max_length=120)
	phone           = models.CharField(blank=True, max_length=12)
	address_line_2  = models.CharField(max_length=120, null=True, blank=True)
	city 			= models.CharField(max_length=120)
	country 		= models.CharField(max_length=120, default="Egypt")
	postal_code     = models.CharField(max_length=120)
	
	# def __Str__(self):
	# 	return str(self.billing_profile)

	def get_address(self):
		return "{for_name}\n{line1}\n{line2}\n{city}".format(
            for_name = self.name or "",
            line1 = self.address_line_1,
            line2 = self.address_line_2 or "",
            city = self.city,
            )
	def __Str__(self):
		return str(self.get_address)