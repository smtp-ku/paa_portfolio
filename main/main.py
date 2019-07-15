from util import alphavantage, data_handle, query

# alphavantage.download_all_data('../data/daily_data/', alphavantage.TimeFlag.DAILY)
# data_handle.make_total_data('../data/daily_data/')
# query.data_insert_test('../data/sample/daily_total.json', 'tb_adj_price_daily')

alphavantage.price_update_from_api()
