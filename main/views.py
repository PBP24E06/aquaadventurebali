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
        )

    # Ambil semua produk untuk ditampilkan di template
    product_list = Product.objects.all()
    return render(request, "main.html", {'data':product_list})

def login(request):
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
    return render(request, "register.html", {})

