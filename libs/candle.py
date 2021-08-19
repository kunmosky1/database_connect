# coding: utf-8
#!/usr/bin/python3

from datetime import timedelta,timezone
import pandas as pd
from libs.database import database

class candle_db:

    def __init__(self, host, key):
        self._db = database( host= host, database='candles', username=key[0], password=key[1], timeout=30 )

    def query_candles( self, exchange, symbol, timescale=1, num_of_candle=2000 ):

        if timescale == 0:
            resolution =1
            num = num_of_candle
        else:
            resolution =timescale
            num = (num_of_candle+2)*timescale+600

        datas = self._db.query( f'select * from candles where time>now()-{num}s and exchange=\'{exchange}\' and symbol=\'{symbol}\'', measurement='candles' )
        df = pd.DataFrame([(self._db.utcstr_to_dt(d['time']),d['open'],d['high'],d['low'],d['close'],d['volume'],d['buy_volume'],d['sell_volume'],
                        d['count'],d['buy_count'],d['sell_count'],d['value'],d['buy_value'],d['sell_value']) for d in datas],
                        columns=["date","open","high","low","close","volume","buy_volume","sell_volume","count","buy_count","sell_count","value","buy_value","sell_value"]
                        ).set_index("date").tz_localize(timezone(timedelta(hours=9),'JST'))

        if timescale == 0:
            return df

        df['close'] = df['close'].fillna(method='ffill')
        df['open'] = df['open'].fillna(df['close'])
        df['high'] = df['high'].fillna(df['close'])
        df['low'] = df['low'].fillna(df['close'])

        df = df.resample(f'{resolution}s').agg(
                          {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum', 'buy_volume': 'sum', 'sell_volume': 'sum',
                           'count': 'sum', 'buy_count': 'sum', 'sell_count': 'sum', 'value': 'sum', 'buy_value': 'sum', 'sell_value': 'sum'})            

        return df.tail(num_of_candle)

    def query_exchanges( self ):
        return [e['value'] for e in self._db.query('show tag values from "candles" with key="exchange"')]
       
    def query_symbols( self, exchange ):
        return [e['value'] for e in self._db.query(f'show tag values from candles with  key="symbol" where exchange=\'{exchange}\'')]

