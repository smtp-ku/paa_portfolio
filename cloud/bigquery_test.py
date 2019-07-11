from google.cloud import bigquery

client = bigquery.Client.from_service_account_json('../stmp-ku-376e736c9bf6.json')

query_job = client.query("""
    select * from `stmp-ku.paa_data.tb_ticker`
""")
results = query_job.result()  # Waits for job to complete.
for row in results:
    print("{} : {} views".format(row.code, row.ticker))
