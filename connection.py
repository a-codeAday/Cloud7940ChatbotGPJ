import pymysql
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def connect():
    return pymysql.connect(host = config['pymysql']['host'],
                           user = config['pymysql']['user'],
                           password = config['pymysql']['password'],
                           database = config['pymysql']['database'],
                           port = config['pymysql'].getint('port'))