from util import query
from datetime import datetime

date_1 = query.get_last_updated_update('tb_adj_price_daily').strftime("%Y-%m-%d")
date_2 = datetime.today().strftime("%Y-%m-%d")

print(date_1)
print(date_2)

if date_1 < date_2:
    print(1)
else:
    print(0)

