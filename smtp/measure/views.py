from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers
from .models import Scenario, InvestReport
from price.models import Compat
from price.views import TimeFlag
import statistics
import operator


def get_start_date(price_data, lookback_period):
    start_date = ""
    for code in price_data:
        code_dates = list(price_data[code].keys())
        if len(code_dates) < lookback_period:
            price_data.pop(code)
        else:
            start_of_code = code_dates[lookback_period]
            if start_of_code > start_date:
                start_date = start_of_code
    return start_date


def get_momentum(target_date, price_data, lookback_period):
    denominator = 0
    for i in range(0, lookback_period+1):
        denominator += i

    result_set = {
        'target_date': target_date
    }
    mom_set = {}

    price_set = {}
    for code in price_data:
        code_price = price_data[code]
        keylist = list(code_price.keys())
        target_index = keylist.index(target_date)
        start_date = keylist[target_index-1]
        result_set['start_date'] = start_date
        code_sma = 0
        for i in range(1, lookback_period+1):
            price = code_price[keylist[target_index-i]]
            code_sma += price*(13-i)/denominator
        code_mom = (code_price[start_date]/code_sma)-1
        price_set[code] = code_mom
    for code in sorted(price_set, key=operator.itemgetter(1), reverse=True):
        mom_set[code] = price_set[code]
    result_set['momentum'] = mom_set
    return result_set


class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = serializers.ScenarioSerializer

    @action(detail=False)
    def make_scenario(self, request):
        params = request.query_params
        if not params.keys() & {'lb', 'codes', 'protection', 'time_flag'}:
            print('not valid')
        else:
            try:
                lookback_period = int(params['lb'])
                ticker_code_list = params['codes'].split(',')
                protection = int(params['protection'])
                if params['time_flag'] == 'daily':
                    time_flag = TimeFlag.DAILY
                elif params['time_flag'] == 'monthly':
                    time_flag = TimeFlag.MONTHLY
                else:
                    raise Exception
            except Exception:
                return Response({'msg': str(Exception)})

        price_data = {}
        if time_flag == TimeFlag.DAILY:
            for ticker_code in ticker_code_list:
                ticker_data = {}
                compat_list = Compat.objects.order_by('date').filter(ticker__code=ticker_code)
                for compat in compat_list:
                    if compat.date.date().strftime('%Y-%m') not in ticker_data:
                        ticker_data[compat.date.date().strftime('%Y-%m')] = []
                    ticker_data[compat.date.date().strftime('%Y-%m')].append(compat.price)
                for month in ticker_data:
                    ticker_data[month] = statistics.mean(ticker_data[month])
                price_data[ticker_code] = ticker_data
        elif time_flag == TimeFlag.MONTHLY:
            for ticker_code in ticker_code_list:
                ticker_data = {}
                compat_list = Compat.objects.order_by('date').filter(ticker__code=ticker_code).filter(isEndofMonth=1)
                for compat in compat_list:
                    ticker_data[compat.date.date().strftime('%Y-%m')] = compat.price
                price_data[ticker_code] = ticker_data

        start_date = get_start_date(price_data, lookback_period)
        test = get_momentum(start_date, price_data, lookback_period)

        return Response(test)


