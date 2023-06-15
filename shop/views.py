from django.shortcuts import render, get_object_or_404, redirect
from .models import Shop
from geopy.distance import geodesic
from django.db.models import Q
import math

def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'list.html', {'shops': shops})

def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    return render(request, 'detail.html', {'shop': shop})

def shop_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        shop = Shop.objects.create(name=name, latitude=latitude, longitude=longitude)
        return redirect('shop_detail', shop_id=shop.id)
    return render(request, 'create.html')

def shop_update(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    if request.method == 'POST':
        shop.name = request.POST['name']
        shop.latitude = request.POST['latitude']
        shop.longitude = request.POST['longitude']
        shop.save()
        return redirect('shop_detail', shop_id=shop.id)
    return render(request, 'update.html', {'shop': shop})

def shop_delete(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    print(request.method)
    if request.method == 'POST':
        shop.name = request.POST['name']
        shop.delete()
        shops = Shop.objects.all()
        return redirect('shop_list')
    return render(request, 'delete.html', {'shop': shop})

def shop_within_distance(request):
    if request.method == 'POST':
        latitude = float(request.POST['latitude'])
        longitude = float(request.POST['longitude'])
        distance = float(request.POST['distance'])

        user_location = (latitude, longitude)
        shops_within_distance = []

        for shop in Shop.objects.all():
            shop_location = (shop.latitude, shop.longitude)
            print("shop_location ", shop_location)
            print("user_location ", user_location)
            print("dist ", dist(user_location, shop_location))
            shop_distance = dist(user_location, shop_location)

            if shop_distance <= distance:
                shops_within_distance.append(shop)

        return render(request, 'within_distance.html', {'shops': shops_within_distance})
    return render(request, 'query_form.html')

def dist(loc1, loc2):
    return math.sqrt(math.pow(loc1[0]-loc2[0], 2) +math.pow(loc1[1]-loc2[1], 2))