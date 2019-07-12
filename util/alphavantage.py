import requests
from util import query
import json
import time
import enum

base_url = "https://www.alphavantage.co/query?"
api_key = "YWK61NRAYQA1IKQ0"


class TimeFlag(enum.Enum):
    DAILY = 0
    MONTHLY = 1


def make_alphavantage_request_url(function_name, symbol):
    request_url = base_url
    request_url += "function=" + function_name
    request_url += "&symbol=" + symbol
    request_url += "&outputsize=full"
    request_url += "&apikey=" + api_key

    return request_url


def request_to_alphavantage(url):
    response = requests.get(url)
    data = response.json()
    return data


def get_monthly_adj_price_by_ticker(ticker):
    result = {}
    global base_data

    try:
        content_key = "Monthly Adjusted Time Series"
        base_data = request_to_alphavantage(make_alphavantage_request_url('TIME_SERIES_MONTHLY_ADJUSTED', ticker))
        monthly_data = base_data[content_key]
        for date in monthly_data:
            result[date] = monthly_data[date]['5. adjusted close']
        current_month = list(result.keys())[0]
        result.pop(current_month)
    except Exception:
        print(base_data)
    return result


def get_daily_adj_price_daily(ticker):
    result = {}
    global base_data

    try:
        content_key = "Time Series (Daily)"
        base_data = request_to_alphavantage(make_alphavantage_request_url('TIME_SERIES_DAILY_ADJUSTED', ticker))
        daily_data = base_data[content_key]
        for date in daily_data:
            result[date] = daily_data[date]['5. adjusted close']
        current_month = list(result.keys())[0]
        result.pop(current_month)
    except Exception:
        print("{} {}".format(ticker, base_data))
    return result


def save_file_as_json(data, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def download_all_data(download_path, time_flag):

    ticker_set = query.get_ticker_dict()

    for ticker_code in ticker_set:
        ticker = ticker_set[ticker_code]
        print(ticker, ticker_code)

        download_data_by_ticker(download_path, ticker_code, ticker, time_flag)

        # if time_flag == TimeFlag.DAILY:
        #     price_data = get_daily_adj_price_daily(ticker)
        #     print('[SYSTEM]: Load Daily_Data Complete')
        # elif time_flag == TimeFlag.MONTHLY:
        #     price_data = get_monthly_adj_price_by_ticker(ticker)
        #     print('[SYSTEM]: Load Monthly_data Complete')
        # save_file_as_json(price_data, download_path + ticker_code + '.json')
        # print('[SYSTEM]: Save Data Complete')
        time.sleep(20)


def download_data_by_ticker(download_path, code, ticker, time_flag):
    if time_flag == TimeFlag.DAILY:
        price_data = get_daily_adj_price_daily(ticker)
        print('[SYSTEM]: Load Daily_Data Complete')
    elif time_flag == TimeFlag.MONTHLY:
        price_data = get_monthly_adj_price_by_ticker(ticker)
        print('[SYSTEM]: Load Monthly_data Complete')

    save_file_as_json(price_data, download_path + code+ '.json')
    print('[SYSTEM]: Save Data Complete')

