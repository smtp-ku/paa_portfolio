from google.cloud import bigquery
import json


def find_data_by_key(data, key):
    if key in data.keys():
        return data[key]
    else:
        return 0


def get_ticker_dict():
    ticker_list = {}
    client = bigquery.Client.from_service_account_json('../smtp-ku-6d028799fd5f.json')
    query_res = client.query("""
        SELECT code, ticker FROM `smtp-ku.paa_data.tb_ticker`
    """).result()
    for res in query_res:
        ticker_list[res.code] = res.ticker
    return ticker_list


def total_data_insert():
    client = bigquery.Client.from_service_account_json('../smtp-ku-6d028799fd5f.json')

    with open('../data/sample/monthly_total.json') as json_file:
        total_data = json.load(json_file)
        for date in total_data:
            print(total_data[date])
            client.query("""
                INSERT INTO `smtp-ku.paa_data.tb_adj_price_monthly`
                (price_date, snp, nasdaq, russell, eurostoxx, topix, mem, mar, wti_idx, agr_idx, silver_idx, gold_idx, high_yield, igb, ltb, skb)
                VALUES (TIMESTAMP("{0}", "US/Eastern"), {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15})
                """.format(
                        date,
                        find_data_by_key(total_data[date], 'snp'),
                        find_data_by_key(total_data[date], 'nasdaq'),
                        find_data_by_key(total_data[date], 'russell'),
                        find_data_by_key(total_data[date], 'eurostoxx'),
                        find_data_by_key(total_data[date], 'topix'),
                        find_data_by_key(total_data[date], 'mem'),
                        find_data_by_key(total_data[date], 'mar'),
                        find_data_by_key(total_data[date], 'wti_idx'),
                        find_data_by_key(total_data[date], 'agr_idx'),
                        find_data_by_key(total_data[date], 'silver_idx'),
                        find_data_by_key(total_data[date], 'gold_idx'),
                        find_data_by_key(total_data[date], 'high_yield'),
                        find_data_by_key(total_data[date], 'igb'),
                        find_data_by_key(total_data[date], 'ltb'),
                        find_data_by_key(total_data[date], 'skb'),
                    )).result()
