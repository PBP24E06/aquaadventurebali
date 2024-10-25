from django.shortcuts import render, reverse, redirect, get_object_or_404
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
from main.models import Product, UserProfile, Forum, User
from main.forms import ForumForm
from django.core.exceptions import PermissionDenied
from functools import wraps

def show_main(request):
    return render(request, "main.html", {})

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

@require_POST
def add_discussion_or_reply(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    parent_id = request.POST.get("parent_id")
    parent_comment = None

    if parent_id:
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

def show_user_discussion(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    discussions = Forum.objects.filter(user=user) 

    context = {
        'user' : user,
        'discussions': discussions,
    }
    
    return render(request, 'show_user_discussion.html', context)
       
def show_xml_forum_by_id(request, id):
    data = Forum.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_forum_by_id(request, id):
    data = Forum.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")