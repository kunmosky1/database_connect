# coding: utf-8
#!/usr/bin/python3

from datetime import timedelta,timezone
import pandas as pd
from libs.database import database

class oi_db:

    def __init__(self, host, key):
        self._db = database(host= host, database='oi', username=key[0], password=key[1], timeout=10)

    def query_oi(self, exchange, period="1d"):

        datas = self._db.query(f'select * from oi where time>now()-{period} and exchange=\'{exchange}\'', measurement='oi')
        df = pd.DataFrame([(self._db.utcstr_to_dt(d['time']),d['open'],d['high'],d['low'],d['close'],
                            d['volume'],d['group'],d['usdbase'],d['btcbase']) for d in datas],
                          columns=["date","open","high","low","close","volume","group","usdbase","btcbase"]
                          ).set_index("date").tz_localize(timezone(timedelta(hours=9),'JST'))

        return df

    def query_exchanges(self):
        return [e['value'] for e in self._db.query('show tag values from "oi" with key="exchange"')]
