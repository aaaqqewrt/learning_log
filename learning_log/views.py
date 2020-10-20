from django.shortcuts import render,redirect
from django.contrib import auth
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User
from django.urls import reverse

