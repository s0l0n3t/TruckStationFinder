from django.db import models

class Station(models.Model):
    opisID = models.IntegerField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    rack_ID = models.IntegerField(max_length=255)
    price = models.IntegerField(max_length=255)