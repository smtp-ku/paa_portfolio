from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Monthly, Daily
from . import serializers

from ticker.models import Ticker
from .util import alphavantage
from datetime import datetime
from . import temp

from pytz import timezone



eastern = timezone('US/Eastern')


class MonthlyViewSet(viewsets.ModelViewSet):
    queryset = Monthly.objects.all()
    serializer_class = serializers.MonthlySerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = ['price_date']

    @action(detail=False)
    def update_price(self, request):
        ticker_set = Ticker.objects.all()
        last_update_date = Monthly.objects.order_by('-price_date').first().price_date
        update_data = {}
        update_result = {}

        # for ticker_object in ticker_set:
        #     recent_data = alphavantage.get_monthly_adj_price_by_ticker(ticker_object.ticker)
        #     for price_date in recent_data:
        #         convert_date = eastern.localize(datetime.strptime(price_date, "%Y-%m-%d"))
        #         if convert_date > last_update_date and convert_date.date() != datetime.now().date():
        #             if price_date not in update_data:
        #                 update_data[price_date] = {}
        #             update_data[price_date][ticker_object.code] = recent_data[price_date]
        #             print(update_data)
        #     print("[SYSTEM]: Update complete {} ({})".format(ticker_object.code, ticker_object.ticker))
        update_data = {'2019-07-15': {'snp': '35490.0000', 'nasdaq': '10345.0000', 'russell': '10420.0000',
                                   'eurostoxx': '11815.0000', 'topix': '13095.0000', 'mem': '10635.0000',
                                   'mar': '13815.0000', 'wti_idx': '4195.0000', 'agr_idx': '4985.0000',
                                   'silver_idx': '3400.0000', 'gold_idx': '10205.0000', 'high_yield': '11730.0000',
                                   'igb': '104630.0000', 'ltb': '11310.0000', 'skb': '56730.0000'}}
        for key in update_data:
            input_data = {}
            prices = update_data[key]
            for code in prices:
                input_data[code] = float(prices[code])
            input_data['price_date'] = datetime.strptime(key, "%Y-%m-%d")
            print(input_data)
            serializer = serializers.MonthlySerializer(data=input_data)
            if serializer.is_valid():
                # serializer.save()
                update_result[key] = update_data[key]
            else:
                print("data is not valid")
        return Response(update_result)


class DailyViewSet(viewsets.ModelViewSet):
    queryset = Daily.objects.all()
    serializer_class = serializers.DailySerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = ['price_date']

    @action(detail=False)
    def update_price(self, request):
        ticker_set = Ticker.objects.all()
        last_update_date = Daily.objects.order_by('-price_date').first().price_date
        update_data = {}

        # for ticker_object in ticker_set:
        #     recent_data = alphavantage.get_daily_adj_price_daily(ticker_object.ticker)
        #     for price_date in recent_data:
        #         convert_date = eastern.localize(datetime.strptime(price_date, "%Y-%m-%d"))
        #         if convert_date > last_update_date and convert_date.date() != datetime.now().date():
        #             if price_date not in update_data:
        #                 update_data[price_date] = {}
        #             update_data[price_date][ticker_object.code] = recent_data[price_date]
        #             print(update_data)
        #     print("[SYSTEM]: Update complete {} ({})".format(ticker_object.code, ticker_object.ticker))

        temp_res = {'2019-07-15': {'snp': '35490.0000', 'nasdaq': '10345.0000', 'russell': '10420.0000',
                                   'eurostoxx': '11815.0000', 'topix': '13095.0000', 'mem': '10635.0000',
                                   'mar': '13815.0000', 'wti_idx': '4195.0000', 'agr_idx': '4985.0000',
                                   'silver_idx': '3400.0000', 'gold_idx': '10205.0000', 'high_yield': '11730.0000',
                                   'igb': '104630.0000', 'ltb': '11310.0000', 'skb': '56730.0000'}}

        return Response(temp_res)
