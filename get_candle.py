# coding: utf-8
#!/usr/bin/python3

from libs import auth_db, candle_db

if __name__ == '__main__':

    host='oi.kumo.tokyo'                                       # 管理人から指定されたホストを記載します
    username = "999999999999999999"                            # DiscordIDを記載します
    password = "ZiL6UW2SV4VHpy-oDnt9QLg5irldnbqdPWwzGbSM2Jg="  # 管理人から提供されたパスワードを記載します
    
    # アクセス用のワンタイムパスワード生成（6時間有効）
    key = auth_db(host).generate_key(username, password)

    # DB接続
    db = candle_db( host, key )

    # ローソク足を取得 timescaleは=秒　取得できる最大本数は約1日分 (timescale*num_of_candle < 86400)
    print( db.query_candles( exchange='Bitflyer', symbol='FX_BTC_JPY', timescale=5, num_of_candle=24*60*12 ) )

    # 取得可能な取引所のリスト　['Binance', 'BinanceSpot', 'Bitflyer', 'Bitmex', 'Bybit', 'Coinbase', 'Deribit', 'Ftx', 'Gmo', 'Huobi', 'Kraken', 'Okex', 'Phemex']
    print( db.query_exchanges() )

    # 取得可能なシンボルのリスト　['BTC_JPY', 'FX_BTC_JPY']...
    print( db.query_symbols('Bitflyer') )
