import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from pymongo import MongoClient
from pymongo import InsertOne
# from hashlib import md5
# import re
# from multiprocessing.dummy import Pool  # This is a thread-based Pool
# from multiprocessing import cpu_count


def get_db():
    if 'db' not in g:
        client = MongoClient('localhost', 27017)
        # print(client.list_database_names())
        db = client["xpcpndt"]
        return db


def init_app(a):
    pass