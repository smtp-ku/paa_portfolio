from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers
from .models import Scenario, InvestReport
from price.models import Compat
from price.views import TimeFlag


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
                    ticker_data[compat.date.date().strftime('%Y-%m-%d')] = compat.price
                price_data[ticker_code] = ticker_data
            return Response(price_data)
        elif time_flag == TimeFlag.MONTHLY:
            for ticker_code in ticker_code_list:
                ticker_data = {}
                compat_list = Compat.objects.order_by('date').filter(ticker__code=ticker_code).filter(isEndofMonth=1)
                for compat in compat_list:
                    ticker_data[compat.date.date().strftime('%Y-%m')] = compat.price
                price_data[ticker_code] = ticker_data
            return Response(price_data)


