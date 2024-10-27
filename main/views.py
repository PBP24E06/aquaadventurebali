from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from main.models import Product, UserProfile, Review, Wishlist, Transaction
from main.forms import ReviewForm, UserProfileForm

from main.models import Product, UserProfile, Report
from django.core.paginator import Paginator
from django.db.models import Q
from main.models import Product, UserProfile, Forum
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib.auth.models import User
from main.forms import TransactionForm
from main.forms import ProductForm, ReportForm
from django.utils.html import strip_tags
from main.forms import ProductForm,TransactionForm
from .forms import ReportForm
from .models import Report, Product
import os
from django.core.paginator import Paginator
from django.db.models import Q
from main.models import Product, UserProfile, Forum
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib.auth.models import User
from main.forms import ProductForm, ForumForm
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from urllib.parse import unquote

from django.core.exceptions import ValidationError
from django.core.validators import validate_email



def show_main(request):
    products = Product.objects.all()
    kategori_filter = request.GET.get('kategori')

    if kategori_filter:
        products = products.filter(kategori=kategori_filter)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    for product in products:
        product.formatted_harga = f"{format(product.harga, ',').replace(',', '.')}"

    if min_price:
        products = products.filter(harga__gte=min_price)

    if max_price:
        products = products.filter(harga__lte=max_price)

    print(f"kategori: {kategori_filter}, min: {min_price}, max: {max_price}")
    print(f"Size: {products.count()}")

    for product in products:
        product.formatted_harga = f"{format(product.harga, ',').replace(',', '.')}"


    ordered_prodct = products.order_by('-harga')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(ordered_prodct, 20) 
    page_obj = paginator.get_page(page_number)
    product = serializers.serialize("json", page_obj)

    context = {
       "data": product,
       "category_list": ['Aksesoris','Boots','Camera','Fin','Fins','Glove','Gloves', 'Hood','Jacket','Mask','Others','Pants','Regulator','Snorkel','Socks','Wetsuit'],
       'has_next': page_obj.has_next(),
       'has_previous': page_obj.has_previous(),
       'num_pages': paginator.num_pages,
       'current_page': page_obj.number,
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
    print("ok")
    form = UserCreationForm(request.POST)

    if form.is_valid():
      user = form.save()
      UserProfile.objects.create(user=user, role='CUSTOMER', profile_picture="static/ikon_botak/foto_ikon.jpg")
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

@login_required(login_url='/login')
def make_admin(request, user_id):  
  if request.user.profile.role == 'CUSTOMER':
    user_profile = UserProfile.objects.get(user_id=user_id)
    user_profile.role = 'ADMIN'
    user_profile.save()
    messages.success(request, f'User {user_profile.user.username} is now an admin!')
  return redirect('main:show_main')


  
@login_required(login_url='/login')
def request_admin(request):  # Form untuk mengubah user menjadi admin

  if request.user.profile.role == 'ADMIN':
    messages.info(request, 'You are already an admin!')
    return redirect('main:show_main')
  
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
     

@login_required(login_url='/login')
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

def show_json_complain(request):
    data = Report.objects.filter(user=request.user)
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
def all_report(request, id):
    product = get_object_or_404(Product, pk=id)
    reports = Report.objects.filter(product=product)
    context = {
        "product": product,
        "reports": reports
    }
    return render(request, "all_report.html", context)

@login_required(login_url='/login')
def checkout(request, id):
  product = Product.objects.get(pk=id)

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
      'form': form
  }
  return render(request, "checkout.html", context)

@login_required(login_url='/login')
def view_transaction_history(request):
  transaction_list = Transaction.objects.filter(user=request.user)

  reviewed_products = set(Review.objects.filter(user=request.user).values_list('product_id', flat=True))
  complained_products = set(Report.objects.filter(user=request.user).values_list('product_id', flat=True))

  for transaction in transaction_list:
    transaction.has_reviewed = transaction.product.id in reviewed_products
    transaction.has_complained = transaction.product.id in complained_products
    transaction.product.formatted_harga = f"{format(transaction.product.harga, ',').replace(',', '.')}"

  context = {
    'transaction_list': transaction_list,
    'user': request.user
    }

  return render(request, "transaction_history.html", context)

@login_required
@admin_required
@csrf_exempt
@require_POST
def add_product_ajax(request):
    name = request.POST.get("name")
    kategori = request.POST.get("kategori")
    harga = request.POST.get("harga")
    toko = request.POST.get("toko")
    alamat = request.POST.get("alamat")
    kontak = request.POST.get("kontak")
    gambar = request.FILES.get("gambar")

    new_product = Product(
        name=name,
        kategori=kategori,
        harga=harga,
        toko=toko,
        alamat=alamat,
        kontak=kontak,
        gambar=gambar
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)



@login_required
@admin_required
def delete_product(request, id):
    product = Product.objects.get(pk = id)
    if product.gambar:
        gambar_path = product.gambar.path
        if os.path.isfile(gambar_path):
            os.remove(gambar_path)

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
    
    try:
        validate_email(email)  # Ini akan memicu ValidationError jika email tidak valid
    except ValidationError:
        return JsonResponse({'error': 'Email tidak valid'}, status=400)

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

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    product.formatted_harga = f"{format(product.harga, ',').replace(',', '.')}"
    product_has_complain = False
    cek_complain = Report.objects.filter(product=product)
    if(cek_complain.count() > 0):
       product_has_complain = True
    return render(request, 'product_detail.html', {'data': product, 'product_has_complain': product_has_complain})

@login_required(login_url='/login')
def profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required(login_url='/login')
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main:profile')  # Redirect ke halaman profil setelah disimpan
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@csrf_exempt
@require_POST
def create_review_by_ajax(request, id):
    product = Product.objects.get(pk=id)
    user = request.user
    rating = request.POST.get("rating")
    review_text = request.POST.get("review_text")
    
    print("Create review by ajax called")

    new_review = Review(
       product = product,
       user = user,
       rating = rating,
       review_text = review_text,
    )
    new_review.save()

    print("new review saved")
    
    
    return HttpResponse(b"CREATED", status=201)

@login_required
@csrf_exempt
def create_report_by_ajax(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.product = product
            report.save()
            return HttpResponse("Complaint submitted successfully!", status=201)
        else:
            return HttpResponse("Failed to submit complaint. Please check the form for errors.", status=400)
    return HttpResponse("Invalid request method.", status=405)
   
   

@require_POST
@login_required
def add_discussion_or_reply(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    parent_id = request.POST.get("parent_id")
    parent_comment = None

    if parent_id and parent_id != 'undefined':
        try:
            parent_comment = Forum.objects.get(id=parent_id)
        except Forum.DoesNotExist:
            return HttpResponse("Parent comment does not exist", status=404)

    form = ForumForm(request.POST, user=request.user, product=product, parent=parent_comment)

    if form.is_valid():
        form.save()
        return HttpResponse(b"CREATED", status=201)
    else:
        return HttpResponse("Form data invalid", status=400)

def show_user_profile_json(request, userId):
   user_profile = UserProfile.objects.filter(user=userId)
   return HttpResponse(serializers.serialize("json", user_profile), content_type="application/json")

def show_forum_json(request, product_id):

    discussions = Forum.objects.filter(product_id=product_id).order_by('-created_at')
    top_level_discussions = discussions.filter(parent=None)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(top_level_discussions, 10) 
    page_obj = paginator.get_page(page_number)
    
    top_level_ids = [discussion.id for discussion in page_obj]
    
    filtered_discussions = discussions.filter(
        Q(id__in=top_level_ids) | Q(parent_id__in=top_level_ids)
    )

    user_requester = None
    if request.user.is_authenticated:
        user_requester = serializers.serialize("json", [request.user])
    else:
        user_requester = "AnonymousUser"

    top_level_data = serializers.serialize("json", page_obj)
    filtered_discussions_data = serializers.serialize("json", filtered_discussions)
    
    return JsonResponse({
        'user_requester': user_requester,
        'top_level_discussions': top_level_data, 
        'discussions': filtered_discussions_data, 
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


def show_user_discussion(request, user_id):
    user = request.user
    user_requested = get_object_or_404(User, pk=user_id)
    profile = UserProfile.objects.get(user_id=user_id)

    context = {
       'profile': profile,
        'user_requested': user_requested,
        'user': user,
    }
    
    return render(request, 'user_discussion.html', context)

def show_user_discussion_json(request, user_id):
    user_requested = get_object_or_404(User, pk=user_id)
    discussions = Forum.objects.filter(user=user_requested).order_by('-created_at')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(discussions, 10)
    page_obj = paginator.get_page(page_number)

    paged_discussion_id = [discussion.id for discussion in page_obj]

    filtered_discussions = discussions.filter(
        Q(id__in=paged_discussion_id) | Q(parent_id__in=paged_discussion_id)
    ).order_by('-created_at')

    discussion_data = []
    for discussion in filtered_discussions:
        product = Product.objects.get(id=discussion.product_id)

        parent_message = discussion.parent.message if discussion.parent else None
        parent_commenter = discussion.parent.commenter_name if discussion.parent else None

        raw_url = product.gambar.url if product.gambar else None
        product_gambar_url = product.gambar.url

        discussion_data.append({
            "pk": discussion.pk,
            "fields": {
                "user_requested" : user_id,
                "product_id": discussion.product_id,
                "product_name": product.name,
                "product_gambar": product_gambar_url,
                "commenter_name": discussion.commenter_name,
                "message": discussion.message,
                "created_at": discussion.created_at.isoformat(),
                "parent": discussion.parent_id,
                "parent_message": parent_message,
                "parent_commenter": parent_commenter
            }
        })

    return JsonResponse({
        'discussions': discussion_data,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })

@require_http_methods(["DELETE"])
def delete_discussion(request, discussion_id):
    discussion = get_object_or_404(Forum, id=discussion_id)
    if request.user != discussion.user:
        return HttpResponseForbidden("You are not allowed to delete this discussion.")
    
    discussion.delete()
    return JsonResponse({"message": "Discussion deleted successfully."})
       
   
@login_required
def show_wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)

    context = {
       "products": wishlists,
       "category_list": ['Aksesoris','Boots','Camera','Fin','Fins','Glove','Gloves', 'Hood','Jacket','Mask','Others','Pants','Regulator','Snorkel','Socks','Wetsuit']
    }
    
    return render(request, "wishlist.html", context)


@csrf_exempt
def filter_wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)

    #Filtering by category
    kategori = request.GET.get('kategori', '')
    if kategori:
      wishlists = wishlists.filter(product__kategori=kategori)

    product_ids = wishlists.values_list('product', flat=True)
    products = Product.objects.filter(id__in=product_ids)

    data = products
    print(data)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def delete_wishlist(request, id):
    product = Product.objects.get(pk=id)
    user = request.user
    wishlist = Wishlist.objects.get(product=product, user=user)
    wishlist.delete()
    return HttpResponseRedirect(reverse('main:show_wishlist'))

@login_required(login_url='/login')
def add_wishlist(request, id):
    product = Product.objects.get(pk=id)
    user = request.user
    try:
      wishlist = Wishlist.objects.get(product=product, user=user)
    except Wishlist.DoesNotExist:
      wishlist = Wishlist(product=product, user=user)
      wishlist.save()
      print(f'Created new wishlist item for product ID: {wishlist.product.id}')
    else:
      print(f'Found existing wishlist item for product ID: {wishlist.product.id}')
    return HttpResponseRedirect(reverse('main:product_detail', args=[id]))
