# TruckStationFinder
Django project

## For using
```
python manage.py runserver
```
and send a post request with ur tool(at least web browser)
http://127.0.0.1:8000/station/find/?latitude=35.6&longitude=-92

latitude = 35.6
longitude = -92

We can set that what are we located in.

## Files

we have an app named station
TruckStationFinder > truckstation > station

Mongodb uses JSON format for collection. So we have a db file
TruckStationFinder > truckstation > database
