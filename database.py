import pymysql


def start_connection():
    db = pymysql.connect("192.168.33.10", "test", "testing123", "test")
    return db.cursor()


def test():
    cursor = start_connection()
    cursor.execute("SELECT * FROM User")
    data = cursor.fetchone()
    print ("Data : %s " % data[1])
    cursor.close()


test()
