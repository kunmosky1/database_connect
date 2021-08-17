# coding: utf-8
#!/usr/bin/python3

from libs import auth_db, oi_db

if __name__ == '__main__':

    # これはサンプルです
    host='hoge.hoge.jp'                                        # 管理人から指定されたホストを記載します
    username = "123456789012345678"                            # DiscordIDを記載します
    password = "abcdefghijklmnopqrstuvqxyz1234567890ABCDEFG="  # 管理人から提供されたパスワードを記載します

    # アクセス用のワンタイムパスワード生成（6時間有効）
    key = auth_db(host).generate_key(username, password)

    # DB接続
    db = oi_db(host, key)

    # ローソク足を取得 pediodは=30m, 4h, 3d, 1w などの取得期間を指定
    print(db.query_oi(exchange='ftx', period="31d"))

    # 取得可能な取引所のリスト　['binance', 'bitmex', 'bybit', 'ftx', 'phemex']
    print(db.query_exchanges())
    
