from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
from bson import json_util
import json

# Create your views here.

def findStation(request):
    cursorObject = stationCollection.find() #Only OK state datas
    listObject = list(cursorObject)
    jsonObject = json_util.dumps(listObject)
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
        }
        for p in listObject
    ]#json list
    # state_list = []
    # for item in product_objects :
    #     if item.get('state') and item.get('state') not in state_list:
    #         state_list.append(item.get('state'))#All states of breakpoints
    return JsonResponse(product_objects,safe=False)

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