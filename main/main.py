import requests

apiKey = "YWK61NRAYQA1IKQ0"
apiDomain = "https://www.alphavantage.co/query?"


def make_request(function_name, symbol):
    request_url = apiDomain+"function=" + str(function_name)+"&symbol=" + str(symbol)+"&apikey=" + str(apiKey)
    return request_url


print(make_request('TIME_SERIES_MONTHLY_ADJUSTED', 'MSFT'))
