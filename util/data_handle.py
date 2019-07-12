import json
from util import query, alphavantage


def make_total_data():
    total_data = {}

    ticker_set = query.get_ticker_dict()
    for ticker_code in ticker_set:
        with open('../data/monthly_data/'+ticker_code+'.json') as json_file:
            json_data = json.load(json_file)
        for date in json_data:
            if date not in total_data:
                total_data[date] = {}
            total_data[date][ticker_code] = json_data[date]

    print(total_data)
    alphavantage.save_file_as_json(total_data, '../data/sample/monthly_total.json')

