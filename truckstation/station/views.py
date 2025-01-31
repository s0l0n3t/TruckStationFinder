from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
from bson import json_util
import json
from .calculation import haversine
from .gmapsroute import generate_google_maps_link

# Create your views here.

def findStation(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    if latitude is None or longitude is None:
        return JsonResponse({
            "error": "Hem 'latitude' hem de 'longitude' parametrelerini sağlamalısınız!"
        }, status=400)

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return JsonResponse({
            "error": "'latitude' ve 'longitude' değerleri geçerli sayılar olmalıdır!"
        }, status=400)

    cursorObject = stationCollection.find()
    listObject = list(cursorObject)

    product_objects = [
        {
            "id": str(p['_id']),  # MongoDB'nin "_id" alanını stringe dönüştür
            "opis_truckstop_id": p.get('OPIS Truckstop ID', None),
            "truckstop_name": p.get('Truckstop Name', None),
            "address": p.get('Address', None),
            "city": p.get('City', None),
            "state": p.get('State', None),
            "rack_id": p.get('Rack ID', None),
            "retail_price": p.get('Retail Price', None),
            "latitude": p.get('latitude', None),
            "longitude": p.get('longitude', None),
        }
        for p in listObject
    ]

    state_list = []

    for item in product_objects:
        if item.get('latitude') is not None and item.get('longitude') is not None:
            distance = haversine(
                float(item.get('latitude')),
                float(item.get('longitude')),
                latitude,
                longitude
            )

            # Eğer mesafe 500 km'den küçükse
            if distance <= 500:
                # JSON'a 'cost' anahtarı ekle
                retail_price = item.get('retail_price', 0) or 0  # Eğer None ise 0 olarak al
                item['cost'] = (distance / 10) * retail_price
                item['distance'] = distance
                item['gmaps_link'] = generate_google_maps_link(latitude,longitude,item.get('latitude'),item.get('longitude'))
                state_list.append(item)

    # 'cost' değerine göre sıralama yap
    sorted_state_list = sorted(state_list, key=lambda x: x['cost'])

    return JsonResponse(sorted_state_list, safe=False)



def findOne(request):
    cursorObject = stationCollection.find() #datas
    listObject = list(cursorObject)
    jsonObject = json_util.dumps(listObject)
    #just a string object
    return JsonResponse(jsonObject,safe=False)

    id = models.ObjectIdField()  # MongoDB'nin "_id" alanı için
    opis_truckstop_id = models.IntegerField()  # "OPIS Truckstop ID" alanı
    truckstop_name = models.CharField(max_length=255)  # "Truckstop Name" alanı
    address = models.TextField()  # "Address" alanı
    city = models.CharField(max_length=100)  # "City" alanı
    state = models.CharField(max_length=2)  # "State" alanı (örnek: VA)
    rack_id = models.IntegerField()  # "Rack ID" alanı
    retail_price = models.DecimalField(max_digits=6, decimal_places=3)  # "Retail Price" alanı