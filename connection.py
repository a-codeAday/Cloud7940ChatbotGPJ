import pymysql
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

def connect():
    return pymysql.connect(host = os.environ['PYMYSQL']['PYMYSQL_HOST'],
                           user = os.environ['PYMYSQL']['PYMYSQL_USER'],
                           password = os.environ['PYMYSQL']['PYMYSQL_PASSWORD'],
                           database = os.environ['PYMYSQL']['PYMYSQL_DB_NAME'],
                           port = os.environ['PYMYSQL'].getint('PYMYSQL_PORT'))
