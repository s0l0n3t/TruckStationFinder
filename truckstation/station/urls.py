from django.urls import path
from . import views

urlpatterns = [
    path('find/',views.findStation),
    path('test/',views.findOne)
]
