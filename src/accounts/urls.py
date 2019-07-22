from django.urls import path, include
from .views import *
urlpatterns = [

	path('login', login_page, name="login"),
	# path('guest/register', guest_register_view, name="guest_register"),
	path('register', register_page , name="register"),
	]