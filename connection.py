import pymysql
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def connect():
    return pymysql.connect(host = config['PYMYSQL']['PYMYSQL_HOST'],
                           user = config['PYMYSQL']['PYMYSQL_USER'],
                           password = config['PYMYSQL']['PYMYSQL_PASSWORD'],
                           database = config['PYMYSQL']['PYMYSQL_DB_NAME'],
                           port = config['PYMYSQL'].getint('PYMYSQL_PORT'))