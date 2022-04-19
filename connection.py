import pymysql
import os

def connect():
    return pymysql.connect(host = os.environ['PYMYSQL_HOST'],
                           user = os.environ['PYMYSQL_USER'],
                           password = os.environ['PYMYSQL_PASSWORD'],
                           database = os.environ['PYMYSQL_DB_NAME'],
                           port = int(os.environ['PYMYSQL_PORT']))
