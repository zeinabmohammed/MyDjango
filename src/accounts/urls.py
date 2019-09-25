from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

	path('login', auth_views.login, name="login"),
	# path('guest/register', guest_register_view, name="guest_register"),
	path('register', register_page , name="register"),
	]