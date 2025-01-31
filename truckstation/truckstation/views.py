from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

def homepage(request):
    return HttpResponse("Hello world!")

def about(request):
    return HttpResponse("Hi folks!")

def route(request):#html response
    return render(request,'home.html')

def testroute(request):#json response
    data = {'name':'Furkan'}
    return JsonResponse(data)