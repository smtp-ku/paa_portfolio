from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone as tz
from .models import Monthly, Daily, Compat
from .permissions import UserPermission
from . import serializers
from .util import alphavantage
from ticker.models import Ticker
from datetime import datetime
from pytz import timezone
from enum import Enum
import calendar

eastern = timezone('US/Eastern')
temp_res = {'2019-07-15': {'snp': '35490.0000', 'nasdaq': '10345.0000', 'russell': '10420.0000',
                           'eurostoxx': '11815.0000', 'topix': '13095.0000', 'mem': '10635.0000',
                           'mar': '13815.0000', 'wti_idx': '4195.0000', 'agr_idx': '4985.0000',
                           'silver_idx': '3400.0000', 'gold_idx': '10205.0000', 'high_yield': '11730.0000',
                           'igb': '104630.0000', 'ltb': '11310.0000', 'skb': '56730.0000'}}


class TimeFlag(Enum):
    DAILY = 0
    MONTHLY = 1


def month_delta(date, delta):
    m, y = (date.month+delta) % 12, date.year + (date.month + delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d, month=m, year=y)


def get_lookback_date(lookback_period):
    return month_delta(tz.now(), (lookback_period * -1));


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CompatViewSet(viewsets.ModelViewSet):
    queryset = Compat.objects.all()
    serializer_class = serializers.CompatSerializer
    filter_backends = [filters.OrderingFilter]


class MonthlyViewSet(viewsets.ModelViewSet):
    queryset = Monthly.objects.all()
    serializer_class = serializers.MonthlySerializer
    filter_backends = [filters.OrderingFilter]
    # permission_classes = [UserPermission]

    def get_queryset(self):
        if 'lb' in self.request.query_params:
            lookback_period = int(self.request.query_params['lb'])
            lookback_date = get_lookback_date(lookback_period)
            self.queryset = Monthly.objects.order_by('-price_date').filter(price_date__gte=lookback_date)
        return self.queryset

    @action(detail=False)
    def update_price(self, request):
        client_ip = get_client_ip(request)
        # Allow only for Cron
        if client_ip == '0.1.0.1':
            ticker_set = Ticker.objects.all()
            last_update_date = Monthly.objects.order_by('-price_date').first().price_date
            update_data = {}
            update_result = {}
            print("[SYSTEM]Last Update Date: "+str(last_update_date))

            for ticker_object in ticker_set:
                recent_data = alphavantage.get_monthly_adj_price_by_ticker(ticker_object.ticker)
                for price_date in recent_data:
                    convert_date = eastern.localize(datetime.strptime(price_date, "%Y-%m-%d"))
                    if convert_date.date() > last_update_date.date() and convert_date.date() != datetime.now().date():
                        if price_date not in update_data:
                            update_data[price_date] = {}
                        update_data[price_date][ticker_object.code] = recent_data[price_date]
                        print(update_data)
                print("[SYSTEM]: Update complete {} ({})".format(ticker_object.code, ticker_object.ticker))

            for key in update_data:
                input_data = {}
                prices = update_data[key]
                for code in prices:
                    input_data[code] = float(prices[code])
                input_data['price_date'] = datetime.strptime(key, "%Y-%m-%d")
                # print(input_data)
                serializer = serializers.MonthlySerializer(data=input_data)
                if serializer.is_valid():
                    serializer.save()
                    update_result[key] = update_data[key]
                else:
                    print("[SYSTEM]: data is not valid")
            return Response(update_result)
        else:
            print("[SYSTEM] Not Cron Request, Request IP: "+str(client_ip))
            return Response({'msg': "Not Cron Request",
                             'IP': str(client_ip)})


class DailyViewSet(viewsets.ModelViewSet):
    queryset = Daily.objects.all()
    serializer_class = serializers.DailySerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        if 'lb' in self.request.query_params:
            lookback_period = int(self.request.query_params['lb'])
            lookback_date = get_lookback_date(lookback_period)
            self.queryset = Daily.objects.order_by('-price_date').filter(price_date__gte=lookback_date)
        return self.queryset

    @action(detail=False)
    def update_price(self, request):
        client_ip = get_client_ip(request)
        # Allow only for Cron
        if client_ip == '0.1.0.1':
            ticker_set = Ticker.objects.all()
            last_update_date = Daily.objects.order_by('-price_date').first().price_date
            update_data = {}
            update_result = {}
            print("[SYSTEM]Last Update Date: "+str(last_update_date))

            for ticker_object in ticker_set:
                recent_data = alphavantage.get_daily_adj_price_daily(ticker_object.ticker)
                for price_date in recent_data:
                    convert_date = eastern.localize(datetime.strptime(price_date, "%Y-%m-%d"))
                    if convert_date.date() > last_update_date.date() and convert_date.date() != datetime.now().date():
                        if price_date not in update_data:
                            update_data[price_date] = {}
                        update_data[price_date][ticker_object.code] = recent_data[price_date]
                        print(update_data)
                print("[SYSTEM]: Update complete {} ({})".format(ticker_object.code, ticker_object.ticker))

            for key in update_data:
                input_data = {}
                prices = update_data[key]
                for code in prices:
                    input_data[code] = float(prices[code])
                input_data['price_date'] = datetime.strptime(key, "%Y-%m-%d")
                # print(input_data)
                serializer = serializers.DailySerializer(data=input_data)
                if serializer.is_valid():
                    serializer.save()
                    update_result[key] = update_data[key]
                else:
                    print("[SYSTEM]: data is not valid")
            return Response(update_result)
        else:
            print("[SYSTEM] Not Cron Request, Request IP: "+str(client_ip))
            return Response({'msg': "Not Cron Request",
                             'IP': str(client_ip)})
