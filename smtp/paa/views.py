from django.shortcuts import render
from django.http import HttpResponse
from .models import Ticker


def show_ticker_description(request):
    return HttpResponse("Ticker Page")


def get_code_all(request):
    code_list = []
    ticker_objects = Ticker.objects.all()
    for obj in ticker_objects:
        code_list.append(obj.code)
    output = '\n'.join(code_list)
    return HttpResponse(output)


def get_ticker_all(request):
    ticker_list = []
    ticker_objects = Ticker.objects.all()
    for obj in ticker_objects:
        ticker_list.append(obj.ticker)
    output = '\r\n'.join(ticker_list)
    return HttpResponse(output)


def get_ticker(request, code):
    return HttpResponse(Ticker.objects.get(code=code).ticker)


