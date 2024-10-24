from django.shortcuts import render, redirect
from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from main.models import Product, UserProfile
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib.auth.models import User
from .forms import CheckoutForm

import pandas as pd
from main.models import Product
import os

def show_main(request):
    product = Product.objects.all()
    return render(request, "main.html", {'data':product})

def login_user(request):
  if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)

    if form.is_valid():
      user = form.get_user()
      login(request, user)
      response = HttpResponseRedirect(reverse("main:show_main"))
      response.set_cookie('last_login', str(datetime.datetime.now()))
      return response
    
    else:
      messages.error(request, "Invalid username or password. Please try again.")

  else:
    form = AuthenticationForm(request)

  context = {'form': form}
  return render(request, 'login.html', context)

def register(request):
  form = UserCreationForm()

  if request.method == "POST":
    form = UserCreationForm(request.POST)

    if form.is_valid():
      user = form.save()
      UserProfile.objects.create(user=user, role='CUSTOMER')
      messages.success(request, 'Your account has been successfully created!')
      return redirect('main:login_user')
    
  context = {'form': form}
  return render(request, 'register.html', context)
    
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login_user'))
    response.delete_cookie('last_login')
    return response

def admin_required(view_func):  # Decorator untuk autentikasi edit & remove product (buat paima)
  @wraps(view_func)
  def _wrapped_view(request, *args, **kwargs):
    try:
      if request.user.profile.role == 'ADMIN':
          return view_func(request, *args, **kwargs)
    except:
      pass
    raise PermissionDenied
  return _wrapped_view

@login_required
def make_admin(request, user_id):  
  if request.user.profile.role == 'CUSTOMER':
    user_profile = UserProfile.objects.get(user_id=user_id)
    user_profile.role = 'ADMIN'
    user_profile.save()
    messages.success(request, f'User {user_profile.user.username} is now an admin!')
  return redirect('main:show_main')


  
# @login_required
def request_admin(request):  # Form untuk mengubah user menjadi admin
  if request.method == 'POST':
    admin_password = request.POST.get('admin_password')

    if admin_password == 'adminpbp':  # Password untuk menjadi admin
      user = request.user

      if user.profile.role == 'CUSTOMER':
        user.profile.promote_admin()
        messages.success(request, 'You have been promoted to admin!')
      else:
        messages.error(request, 'You are already an admin!')

    else:
      messages.error(request, 'Incorrect admin password!')

    return redirect('main:show_main')
  
  return render(request, 'request_admin.html', {})

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def checkout(request, id):
  product = Product.objects.get(pk=id)
  total_harga = product.harga + 10000
  
  if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Simpan data ke Cart atau lakukan proses lainnya
            cart = form.save(commit=False)  # Buat instance Cart tanpa menyimpan ke database
            cart.product = product  # Hubungkan produk dengan cart
            cart.save()  # Simpan cart ke database
            return redirect('some_success_url')  # Redirect setelah penyimpanan sukses
  else:
      form = CheckoutForm()

  context = {'product': product, 'total_harga': total_harga, 'form': form}
  return render(request, "checkout.html", context)
