# coding: utf-8
#!/usr/bin/python3

from cryptography.fernet import Fernet
from datetime import datetime,timedelta
from dateutil import parser
from hashlib import sha256
import hmac
from influxdb import InfluxDBClient
import urllib3

class database:
    def __init__(self, host, database='auth', username='bfsx2', password='user'):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._client = InfluxDBClient(host=host, port=8085, database=database, timeout=5, ssl=True, username=username, password=password)

    def query( self, query, measurement=None ):
        result = self._client.query(query)
        return list(result.get_points(measurement=measurement))

    def utcstr_to_dt(self, date_line):
        try:
            exec_date = date_line.replace('T', ' ')[:-1]
            exec_date = exec_date + '00000000'
            d = datetime(int(exec_date[0:4]), int(exec_date[5:7]), int(exec_date[8:10]), int(exec_date[11:13]),
                         int(exec_date[14:16]), int(exec_date[17:19]), int(exec_date[20:26])) + timedelta(hours=9)
        except :
            d = (parser.parse(date_line) + timedelta(hours=9)).replace(tzinfo=None)
        return d

class auth_db(database):
 
    def generate_key(self, username, password):
        self.__hash_code = hmac.new(username.encode('utf-8'), password.encode('utf-8'), sha256).hexdigest()
        res = self.query("select last(*) from hashlist where hash_code='"+self.__hash_code+"'", measurement="hashlist" )
        if not res:
            raise ValueError("Authentification Error!")
        f = Fernet(password)
        return (f.decrypt(res[0]['last_user_token'].encode()), f.decrypt(res[0]['last_pw_token'].encode()))

