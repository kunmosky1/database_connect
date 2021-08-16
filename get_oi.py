# coding: utf-8
#!/usr/bin/python3

from libs import auth_db, oi_db

if __name__ == '__main__':

    host='oi.kumo.tokyo'
    username = "123456789012345678"                            # DiscordIDを指定します
    password = "abcdefghijklmnopqrstuvqxyz1234567890ABCDEFG="  # 管理人から提供されたパスワードを指定します

    # アクセス用のワンタイムパスワード生成（１日間有効）
    key = auth_db( host ).generate_key( username, password )

    # DB接続
    db = oi_db( host, key )

    # ローソク足を取得 pediodは=30m, 4h, 3d, 1w などの取得期間を指定
    print( db.query_oi( exchange='ftx', period="31d" ) )

    # 取得可能な取引所のリスト　['binance', 'bitmex', 'bybit', 'ftx', 'phemex']
    print( db.query_exchanges() )
    
