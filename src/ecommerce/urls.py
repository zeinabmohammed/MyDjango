
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from .views import home_page, about_page, contact_page
from django.contrib.auth.views import LogoutView
from accounts.views import login_page, register_page#, guest_register_view
from addresses.views import checkout_address_create_view
urlpatterns = [
	path('', home_page, name="home"),
	path('about/', about_page, name="about"),
	path('contact/', contact_page, name="contact"),
	#path(r'contact/view', contact_page),
	path('checkout/address/create', checkout_address_create_view, name="ckeckout_address_create"),
	path('login', login_page, name="login"),
	# path('register_guest', guest_register_view, name="guest_register"),
	path('logout/', LogoutView.as_view(), name="logout"),
	path('register', register_page , name="register"),
	path('bootstrap',TemplateView.as_view(template_name="bootstrap/example.html")),
	path('products/', include("products.urls")),
	path('search/', include("search.urls")),
	path('cart/', include("carts.urls")),
	# path('cart/', cart_home, name="cart"),
	path('admin/', admin.site.urls),

    ]
if settings.DEBUG:
	urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
