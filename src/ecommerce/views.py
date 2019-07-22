from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import ContactForm, LoginForm, RegisterForm


def home_page(request):
	# print(request.session.get("first_name","unknown"))
	context = {
	"title": "hello world"	,
	"content": "Welcome to home page",

	}
	if (request.user.is_authenticated):
		context["premium_content"] = "YAAAH"

	return render(request, "home_page.html", context)


def about_page(request):
	context = {
	"title": "About!"
	}

	return render(request, "about_page.html", context)


def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
	"title": "Contact us!",
	"form": contact_form,
	
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
	# if request.method == "POST":
		# print(request.POST)
		# print(request.POST.get('fullname'))
		# print(request.POST.get('Email'))
		# print(request.POST.get('content'))
	return render(request, "contact/view.html", context)


# def login_page(request):
# 	form = LoginForm(request.POST or None)
# 	context = {
# 			"form": form
# 			}
# 	# print("user authenticated")
# 	if form.is_valid():
# 		print(form.cleaned_data)
# 		username = form.cleaned_data.get("username")
# 		password = form.cleaned_data.get("password")
# 		user = authenticate(request, username=username, password=password)
# 		print(user)
# 		if user is not None:
# 			login(request, user)
# 			return(redirect("/home"))
# 		else:
# 		    print("Error!")
		
# 	return render(request, "auth/login.html",context)



# User = get_user_model()
# def register_page(request):
# 	form = RegisterForm(request.POST or None)
# 	context = {
# 			"form": form
# 			}
# 	if form.is_valid():
# 		print(form.cleaned_data)
# 		username = form.cleaned_data.get("username")
# 		Email 	 = form.cleaned_data.get("email")
# 		password = form.cleaned_data.get("password")
		
# 		new_user = User.objects.create_user(username, email, password)
# 		print(new_user)
# 		#User.objects.create_user(username, email, password)
# 	return render(request, "auth/register.html",context)	
