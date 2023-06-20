from django.shortcuts import render, get_object_or_404, redirect
from .models import Shop
import math
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.decorators import login_required



SECRET_KEY = "secret"

@csrf_exempt
def register(request):
    # API Endpoint for registering user
    if request.method == 'POST':
        # Process the registration form data
        username = request.POST['username']
        password = request.POST['password']
        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        # Redirect to a success page or login the user
        return redirect('login')
    else:
        return render(request, 'register.html')

def login_view(request):
    # API Endpoint for Login
    message=""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print("user: ", user == "AnonymousUser")
        if user is not None or user == "AnonymousUser":
            login(request, user)
            return redirect('shop_list')
        message = "Incorrect Username or Password"
    return render(request, 'login.html', {"message":message})

def user_logout(request):
    # API Endpoint for logout
    logout(request)
    return redirect('login')

@csrf_exempt
@permission_classes([IsAuthenticated])
@login_required(login_url='login')
def shop_list(request):
    # API Endpoint for Fetching shop list
    shops = Shop.objects.all()
    print("user ", request.user)
    print("user: ", request.user == "AnonymousUser")
    return render(request, 'list.html', {'shops': shops})

@csrf_exempt
@permission_classes([IsAuthenticated])
@login_required(login_url='login')
def shop_detail(request, shop_id):
    # API Endpoint for fetching shop details
    shop = get_object_or_404(Shop, pk=shop_id)
    return render(request, 'detail.html', {'shop': shop})

@csrf_exempt
@permission_classes([IsAuthenticated])
@login_required(login_url='login')
def shop_create(request):
    # API Endpoint for Creating new shop
    # payload = {"name":"", "latitude":"", "longitude":""}
    if request.method == 'POST':
        name = request.POST['name']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        shop = Shop.objects.create(name=name, latitude=latitude, longitude=longitude)
        return redirect('shop_detail', shop_id=shop.id)
    return render(request, 'create.html')

@csrf_exempt
@permission_classes([IsAuthenticated])
@login_required(login_url='login')
def shop_update(request, shop_id):
    # API Endpoint for updating shop details
    # payload = {"name":"", "latitude":"", "longitude":""}
    shop = get_object_or_404(Shop, pk=shop_id)
    if request.method == 'POST':
        shop.name = request.POST['name']
        shop.latitude = request.POST['latitude']
        shop.longitude = request.POST['longitude']
        shop.save()
        return redirect('shop_detail', shop_id=shop.id)
    return render(request, 'update.html', {'shop': shop})

@csrf_exempt
@permission_classes([IsAuthenticated])
@login_required(login_url='login')
def shop_delete(request, shop_id):
    # API Endpoint for Deleting existing shop
    shop = get_object_or_404(Shop, pk=shop_id)
    if request.method == 'POST':
        shop.name = request.POST['name']
        shop.delete()
        shops = Shop.objects.all()
        return redirect('shop_list')
    return render(request, 'delete.html', {'shop': shop})

@csrf_exempt
@permission_classes([IsAuthenticated])
@login_required(login_url='login')
def shop_within_distance(request):
    # API Endpoint for fetching shops in given radius from given location
    # Payload = {"distance":"", "latitude":"", "longitude":""}
    if request.method == 'POST':
        latitude = float(request.POST['latitude'])
        longitude = float(request.POST['longitude'])
        distance = float(request.POST['distance'])

        user_location = (latitude, longitude)
        shops_within_distance = []

        for shop in Shop.objects.all():
            shop_location = (shop.latitude, shop.longitude)
            shop_distance = dist(user_location, shop_location)

            if shop_distance <= distance:
                shops_within_distance.append(shop)

        return render(request, 'within_distance.html', {'shops': shops_within_distance})
    return render(request, 'query_form.html')

def dist(loc1, loc2):
    return math.sqrt(math.pow(loc1[0]-loc2[0], 2) +math.pow(loc1[1]-loc2[1], 2))