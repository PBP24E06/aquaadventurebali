from django.shortcuts import render, redirect
from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
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
from main.models import Product, UserProfile, Review, Transaction
from main.forms import ReviewForm


from main.models import Product, UserProfile
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib.auth.models import User
from main.forms import TransactionForm
from main.forms import ProductForm
from django.utils.html import strip_tags



def show_main(request):
    products = Product.objects.all()

    # Filtering by category
    kategori_filter = request.GET.get('kategori')

    if kategori_filter:
        products = products.filter(kategori=kategori_filter)

    # Filtering by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(harga__gte=min_price)

    if max_price:
        products = products.filter(harga__lte=max_price)

    print(f"kategori: {kategori_filter}, min: {min_price}, max: {max_price}")

    print(f"Size: {products.count()}")

    context = {
       "data": products,
       "category_list": ['Aksesoris','Boots','Camera','Fin','Fins','Glove','Gloves', 'Hood','Jacket','Mask','Others','Pants','Regulator','Snorkel','Socks','Wetsuit']
    }
    
    return render(request, "main.html", context)

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
    response = HttpResponseRedirect(reverse('main:show_main'))
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


  
@login_required
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

@login_required
def create_review(request, id):
  form = ReviewForm(request.POST or None)
  product = Product.objects.get(pk=id)
  if request.method == "POST":
    print("POST data:", request.POST)  # Debug print
    if form.is_valid():
      review = form.save(commit=False)
      review.user = request.user
      review.product = product
      review.save()
      return redirect("main:show_main")
    else:
      print( form.errors)
  
  context = {
    "form": form,
    "product": product
  }
     
  return render(request, "review_form.html", context)


def show_json_product(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_transaction(request):
    data = Transaction.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")



@login_required(login_url='/login')
def all_review(request, id):
    product = Product.objects.get(pk=id)
    reviews = product.reviews.all()
    context = {
      "product": product,
      "reviews": reviews
    }
    return render(request, "all_review.html", context)

@login_required(login_url='/login')
def checkout(request, id):
  product = Product.objects.get(pk=id)
  total_harga = product.harga + 10000

  if request.method == 'POST':
      form = TransactionForm(request.POST)
      if form.is_valid():
          # Process form data here, e.g., save the order, send an email, etc.
          transaction = form.save(commit=False)
          transaction.product = product
          transaction.user = request.user
          transaction.save()
          return redirect('main:show_main')

  else:
      form = TransactionForm()


  context = {
      'product': product,
      'total_harga': total_harga,
      'form': form
  }
  return render(request, "checkout.html", context)

@login_required(login_url='/login')
def view_transaction_history(request):
  transaction_list = Transaction.objects.filter(user=request.user)

  context = {'transaction_list': transaction_list}

  return render(request, "transaction_history.html", context)

@login_required
@admin_required
def create_product(request):
  form = ProductForm(request.POST or None )

  if form.is_valid() and request.method == "POST":
    form.save()
    return redirect('main:show_main')
  
  context = {'form': form}
  return render(request, "create_product.html", context)

@login_required
@admin_required
def delete_product(request, id):
    product = Product.objects.get(pk = id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required
@admin_required
def edit_product(request, id):
    product = Product.objects.get(pk = id)

    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)


@csrf_exempt
@require_POST
def checkout_by_ajax(request, id):
    name = strip_tags(request.POST.get("name"))
    email = strip_tags(request.POST.get("email"))
    phone_number = strip_tags(request.POST.get("phone_number"))
    product = Product.objects.get(pk=id)
    user = request.user
    

    new_transaction = Transaction(
        name=name, email=email,
        phone_number=phone_number,
        product=product, user=user
    )
    new_transaction.save()

    return HttpResponse(b"CREATED", status=201) 

def get_product_data_for_checkout(request, id):
    product = Product.objects.get(pk=id)
    data = {
        'name': product.name,
        'gambar': product.gambar.url,
        'harga': product.harga,
    }
    return JsonResponse(data)  
