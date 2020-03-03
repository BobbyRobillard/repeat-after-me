import pymysql


def start_connection():
    db = pymysql.connect("192.168.33.10", "test", "testing123", "test")
    return db
