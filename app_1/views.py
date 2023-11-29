from django.http import HttpResponse
from django.shortcuts import render

def url1(request):
    return HttpResponse("Ответ 1")

def url2(request):
    return HttpResponse("Ответ 2")

