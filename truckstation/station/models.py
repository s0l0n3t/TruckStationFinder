from django.db import models
from station.dbconnection import db



stationCollection = db['stationdb']

from djongo import models

class Truckstop(models.Model):
    id = models.ObjectIdField()  # MongoDB'nin "_id" alanı için
    opis_truckstop_id = models.IntegerField()  # "OPIS Truckstop ID" alanı
    truckstop_name = models.CharField(max_length=255)  # "Truckstop Name" alanı
    address = models.TextField()  # "Address" alanı
    city = models.CharField(max_length=100)  # "City" alanı
    state = models.CharField(max_length=2)  # "State" alanı (örnek: VA)
    rack_id = models.IntegerField()  # "Rack ID" alanı
    retail_price = models.DecimalField(max_digits=6, decimal_places=3)  # "Retail Price" alanı

    class Meta:
        db_table = "stationdb"  # MongoDB'deki koleksiyon adı

    def __str__(self):
        return f"{self.truckstop_name} - {self.city}, {self.state}"


# opisID = models.IntegerField(max_length=255)
#     name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     state = models.CharField(max_length=255)
#     rack_ID = models.IntegerField(max_length=255)
#     price = models.IntegerField(max_length=255)