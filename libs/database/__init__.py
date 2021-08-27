# coding: utf-8
#!/usr/bin/python3

__all__ = ['auth_db', 'oi_db', 'candle_db']

from .db_server import auth_db
from .oi import oi_db
from .candle import candle_db
