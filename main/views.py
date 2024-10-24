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

import pandas as pd
from main.models import Product
import os

def show_main(request):
    # Path file CSV
    csv_file_path = os.path.join('static', 'data', 'data.csv')

    # Membaca CSV menggunakan pandas
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        return HttpResponse("File CSV tidak ditemukan.")
    except Exception as e:
        return HttpResponse(f"Error membaca file CSV: {str(e)}")

    # Simpan data dari CSV ke database
    for index, row in df.iterrows():
        Product.objects.create(
            name=row['name'],
            kategori=row['kategori'],
            harga=row['harga'],
            toko=row['toko'],
            alamat=row['alamat'],
            kontak=row['kontak'],
            gambar=row['gambar']
        )

    # Ambil semua produk untuk ditampilkan di template
    product_list = Product.objects.all()
    return render(request, "main.html", {'data':product_list})

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
  response = HttpResponseRedirect(reverse("main:login_user"))
  response.delete_cookie("last_login")
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

def checkout(request, id):
  product = Product.objects.get(pk=id)
  total_harga = product.harga + 10000
  context = {'product': product, 'total_harga': total_harga}
  return render(request, "checkout.html", context)
