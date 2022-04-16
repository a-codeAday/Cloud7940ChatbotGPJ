import pymysql
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

def connect():
    return pymysql.connect(host = os.environ['PYMYSQL_HOST'],
                           user = os.environ['PYMYSQL_USER'],
                           password = os.environ['PYMYSQL_PASSWORD'],
                           database = os.environ['PYMYSQL_DB_NAME'],
                           port = os.environ['PYMYSQL_PORT'])
