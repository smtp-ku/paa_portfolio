import requests
from util import query
import json
import time
import enum
from datetime import datetime
from tqdm import tqdm
from pytz import timezone

base_url = "https://www.alphavantage.co/query?"
api_key = "YWK61NRAYQA1IKQ0"
call_interval = 15
eastern = timezone('US/Eastern')


class TimeFlag(enum.Enum):
    DAILY = 0
    MONTHLY = 1


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
        first_key = list(result.keys())[0]
        result.pop(first_key)
    except Exception:
        print("{} {}".format(ticker, base_data))

    # for alphavantage policy
    # time.sleep(call_interval)
    wait_for_call(call_interval)
    return result


def get_daily_adj_price_daily(ticker):
    result = {}
    global base_data

    try:
        content_key = "Time Series (Daily)"
        base_data = request_to_alphavantage(make_alphavantage_request_url('TIME_SERIES_DAILY_ADJUSTED', ticker))
        daily_data = base_data[content_key]
        # refresh_date = base_data["Meta Data"]["3. Last Refreshed"]
        # refresh_date = eastern.localize(datetime.strptime(base_data["Meta Data"]["3. Last Refreshed"], "%Y-%m-%d"))
        for date in daily_data:
            result[date] = daily_data[date]['5. adjusted close']
        first_key = list(result.keys())[0]
        result.pop(first_key)
    except Exception:
        print("{} {}".format(ticker, base_data))

    # for alphavantage policy
    # time.sleep(call_interval)
    wait_for_call(call_interval)
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


def download_data_by_ticker(download_path, code, ticker, time_flag):
    if time_flag == TimeFlag.DAILY:
        price_data = get_daily_adj_price_daily(ticker)
        print('[SYSTEM]: Load Daily_Data Complete')
    elif time_flag == TimeFlag.MONTHLY:
        price_data = get_monthly_adj_price_by_ticker(ticker)
        print('[SYSTEM]: Load Monthly_data Complete')

    save_file_as_json(price_data, download_path + code+ '.json')
    print('[SYSTEM]: Save Data Complete')


def wait_for_call(interval):
    for _ in tqdm(range(0, interval)):
        time.sleep(1)


def price_update_from_api():

    update_daily = {}
    update_monthly = {}

    ticker_set = query.get_ticker_dict()
    last_updated_date = query.get_last_updated_update('tb_adj_price_daily')
    # last_updated_date = datetime.strptime("2019-07-09", "%Y-%m-%d")

    print("[SYSTEM]: Start updating daily data from {}".format(last_updated_date))
    for code in ticker_set:
        recent_data = get_daily_adj_price_daily(ticker_set[code])
        for price_date in recent_data:
            convert_date = eastern.localize(datetime.strptime(price_date, "%Y-%m-%d"))
            if convert_date > last_updated_date and convert_date.date() != datetime.now().date():
                if price_date not in update_daily:
                    update_daily[price_date] = {}
                update_daily[price_date][code] = recent_data[price_date]
                print(update_daily)
        print("[SYSTEM]: Update complete {} ({})".format(code, ticker_set[code]))
    print(update_daily)
    query.data_insert(update_daily, 'tb_adj_price_daily')

    print("[SYSTEM]: Start updating monthly data from {}".format(last_updated_date))
    for code in ticker_set:
        recent_data = get_monthly_adj_price_by_ticker(ticker_set[code])
        for price_date in recent_data:
            convert_date = eastern.localize(datetime.strptime(price_date, "%Y-%m-%d"))
            if convert_date > last_updated_date and convert_date.date() != datetime.now().date():
                if price_date not in update_monthly:
                    update_monthly[price_date] = {}
                update_monthly[price_date][code] = recent_data[price_date]
        print("[SYSTEM]: Update complete {} ({})".format(code, ticker_set[code]))
    print(update_monthly)
    query.data_insert(update_monthly, 'tb_adj_price_monthly')







