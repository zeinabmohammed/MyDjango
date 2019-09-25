from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import  AuthenticationForm
from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import  LoginForm, RegisterForm#, GuestForm
from django.utils.http import is_safe_url
from django.contrib import messages 
from django.contrib import messages 


def login_page(request):
	form = LoginForm(data=request.POST)
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
			messages.add_message(request, messages.INFO, "You are now logged-In, welcome")
			user_url = is_safe_url(redirect_path, request.get_host())
			print (user_url)
			if  is_safe_url(redirect_path, request.get_host()):
				return(redirect(redirect_path))
		else:
			messages.error(request,'username or password not correct')
			return redirect('login')

			args = {'form': form}
			# messages.error(request, "Error")
			# return (redirect('/'))
	# else:
	# 	form=LoginForm()
	
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
