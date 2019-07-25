from rest_framework import viewsets, pagination
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers
from .models import Scenario, Portfolio
from price.models import Compat
from price.views import TimeFlag
from datetime import datetime
import statistics
import operator


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = serializers.ScenarioSerializer
    pagination_class = LargeResultsSetPagination

    @action(detail=False)
    def make_scenario(self, request):

        # Validate Parameters
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

        result = {
            'lookback_period': lookback_period,
            'ticker_list': ticker_code_list,
            'protection_degree': protection,
            'time_flag': params['time_flag'],
            'created_date': datetime.now()
        }
        # TODO Scenario serialize

        # Make Price Data for Portfolio
        price_data = make_price_data(ticker_code_list, time_flag)

        # Make Target List
        target_list = make_target_list(price_data, lookback_period)

        # Make Portfolio
        portfoilo = {}
        for target_date in target_list:
            # TODO Portfolio Serialize
            portfoilo[target_date] = make_portfolio(target_date, price_data, lookback_period, protection, ref_num=6)
        result['portfolio'] = portfoilo

        return Response(result)


def make_price_data(ticker_code_list, time_flag):
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
    return price_data


def make_target_list(price_data, lookback_period):
    start_date = ""
    end_date = ""
    for code in price_data:
        code_dates = list(price_data[code].keys())
        if len(code_dates) < lookback_period:
            price_data.pop(code)
        else:
            start_of_code = code_dates[lookback_period]
            end_of_code = code_dates[len(code_dates)-1]
            if start_of_code > start_date:
                start_date = start_of_code
            if end_of_code < end_date or end_date == "":
                end_date = end_of_code
    standard_price = price_data[list(price_data.keys())[0]]
    target_list = []
    for date in standard_price:
        if start_date < date <= end_date:
            target_list.append(date)
    return target_list


def get_bond_ratio(asset_cnt, positive_cnt, protection_degree):
    protection_value = (protection_degree*asset_cnt)/4
    denominator = asset_cnt - protection_value
    numerator = asset_cnt - positive_cnt
    ratio = numerator / denominator
    return ratio


def get_average_price(ticker_code, target_date):
    year = target_date.split('-')[0]
    month = target_date.split('-')[1]

    month_data = Compat.objects.filter(
        ticker__code=ticker_code,
        date__year__gte=year,
        date__month__gte=month,
        date__year__lte=year,
        date__month__lte=month
    )
    month_price_list = []
    for data in month_data:
        month_price_list.append(float(data.price))
    return statistics.mean(month_price_list)


def make_portfolio(target_date, price_data, lookback_period, protection, ref_num=6):

    # Initialize
    result_set = {}
    mom_set = {}
    portfolio = {}
    positive_cnt = 0
    denominator = 0
    for i in range(0, lookback_period+1):
        denominator += i

    # Calculate Momentum
    for code in price_data:
        code_price = price_data[code]
        date_list = list(code_price.keys())

        if target_date not in date_list:
            date_list.append(target_date)
            date_list.sort()
            code_price[target_date] = get_average_price(code, target_date)

        target_index = date_list.index(target_date)
        start_date = date_list[target_index-1]
        code_sma = 0
        for i in range(1, lookback_period+1):
            price = code_price[date_list[target_index-i]]
            code_sma += price*(lookback_period+1-i)/denominator
        code_mom = (code_price[start_date]/code_sma)-1
        if code_mom > 0:
            positive_cnt += 1
        mom_set[code] = code_mom

    # Calculate Bond Ratio
    if positive_cnt >= ref_num:
        bond_ratio = get_bond_ratio(len(price_data), ref_num, protection)
    else:
        bond_ratio = 1
    asset_ratio = 1 - bond_ratio

    # Make Portfolio
    sorted_mom = sorted(mom_set.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(0, ref_num):
        portfolio[sorted_mom[i][0]] = asset_ratio/ref_num

    # Calculate Revenue
    total_revenue = 0
    for code in portfolio:
        code_price = price_data[code]
        target_index = date_list.index(target_date)
        start_price = code_price[date_list[target_index - 1]]
        target_price = code_price[date_list[target_index]]
        code_revenue = (target_price-start_price)/start_price * portfolio[code]
        total_revenue += code_revenue

    # Make Result
    result_set['momentum'] = mom_set
    result_set['isInvestable'] = positive_cnt >= ref_num
    result_set['bond_ratio'] = bond_ratio
    result_set['portfolio'] = portfolio
    if datetime.now().strftime("%Y-%m") == target_date:
        result_set['revenue'] = "Not yet"
    else:
        result_set['revenue'] = total_revenue

    return result_set



