from django.shortcuts import render,redirect
from django.contrib import auth
from .forms import LoginForm,RegForm
# ~ from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model

User=get_user_model()
def login(request):
	if request.method == 'POST':
		login_form=LoginForm(request.POST)
		if login_form.is_valid():
			user=login_form.cleaned_data['user']
			auth.login(request,user)
			return redirect(request.GET.get('from',reverse('learning_logs:index')))	
	else:	
		login_form=LoginForm()
		
	context={}
	context['login_form']=login_form
	return render(request, 'user/login.html',context)

def register(request):
	if request.method == 'POST':
		reg_form=RegForm(request.POST)
		if reg_form.is_valid():
			username=reg_form.cleaned_data['username']
			email=reg_form.cleaned_data['email']
			password=reg_form.cleaned_data['password']
			#创建用户
			user=User.objects.create_user(username,email,password)
			user.save()
			
			'''
			user=User()
			user.username=username
			user.set_password(password)
			user.email=email
			user.save()
			'''
			#登录用户
			user=auth.authenticate(username=username,password=password)
			auth.login(request,user)
			return redirect(request.GET.get('from',reverse('learning_logs:index')))				
	else:	
		reg_form=RegForm()
		
	context={}
	context['reg_form']=reg_form
	return render(request, 'user/register.html',context)	

def logout(request):
	auth.logout(request)
	return redirect(request.GET.get('from',reverse('learning_logs:index')))	


def user_info(request):
	context={}
	return render(request,'user/user_info.html',context)




















