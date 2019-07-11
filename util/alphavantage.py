import requests
from util import query
import json
import time

base_url = "https://www.alphavantage.co/query?"
api_key = "YWK61NRAYQA1IKQ0"


def make_alphavantage_request_url(function_name, symbol):
    request_url = base_url
    request_url += "function=" + function_name
    request_url += "&symbol=" + symbol
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


def save_file_as_json(data, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def download_all_data():
    ticker_set = query.get_ticker_dict()

    for ticker_code in ticker_set:
        ticker = ticker_set[ticker_code]
        print(ticker, ticker_code)
        price_data = get_monthly_adj_price_by_ticker(ticker)
        print('get monthly_data complete')
        save_file_as_json(price_data, '../monthly_data/' + ticker_code + '.json')
        print('save monthly_data complete')
        time.sleep(20)


def download_data_by_ticker(code, ticker):
    price_data = get_monthly_adj_price_by_ticker(ticker)
    save_file_as_json(price_data, '../data/monthly_data/' + code+ '.json')

