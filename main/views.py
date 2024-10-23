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
from main.models import Product
from main.forms import ProductForm, ReviewForm

def show_main(request):
  return render(request, "main.html", {})

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

def create_review(request, id):
  form = ReviewForm(request.POST or None)
  product = Product.objects.filter(pk=id)

  if form.is_valid() and request.method == "POST":
    review = form.save(commit=False)
    review.user = request.user
    review.save()
    return redirect("main:show_main")
  
  context = {
    "form": form,
    "product": product
  }
     
  return render(request, "review.html", context)