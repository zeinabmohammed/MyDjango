from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import  AuthenticationForm
from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import  LoginForm, RegisterForm#, GuestForm
from django.utils.http import is_safe_url
from django.contrib import messages 
# from .models import GuestEmail
# def guest_register_view(request):
# 	form = GuestForm(request.POST or None)
# 	context = {
# 			"form": form,
# 			}
# 	next_get_url= request.GET.get('next')
# 	next_post_url= request.POST.get('next')
# 	redirect_path = next_get_url or next_post_url or None
# 	if form.is_valid():
# 		cv=request.get_host()
# 		print(cv)
# 		# print(form.cleaned_data)
# 		email = form.cleaned_data.get("email")
# 		new_guest_email = GuestEmail.objects.create(email=email)
# 		request.session['guest_id']=new_guest_email.id
# 		if  is_safe_url(redirect_path, request.get_host()):
# 			return(redirect(redirect_path))
# 		else:
# 			return (redirect('/register/'))
# 	else:
# 		messages.error(request, 'Error wrong username/password')
	
# 	return render(request, "/register/",context)

def login_page(request):
	form = LoginForm(request.POST or None)
	context = {
			"form": form,
			}
	next_get_url= request.GET.get('next')
	next_post_url= request.POST.get('next')
	redirect_path = next_get_url or next_post_url or None
	if form.is_valid():
		# print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		print(user)
		if user is not None:
			login(request, user)
			user_url = is_safe_url(redirect_path, request.get_host())
			print (user_url)
			if  is_safe_url(redirect_path, request.get_host()):
				return(redirect(redirect_path))
		else:
			return (redirect('/'))
	else:
		messages.error(request, 'Error wrong username/password')
	
	return render(request, "accounts/login.html",context)



User = get_user_model()
def register_page(request):
	form = RegisterForm(request.POST or None)
	context = {
			"form": form
			}
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		email 	 = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		
		new_user = User.objects.create_user(username, email, password)
		print(new_user)
		#User.objects.create_user(username, email, password)
	return render(request, "accounts/register.html",context)	
