import pymysql


def start_connection():
    db = pymysql.connect("68.183.125.253", "test", "testing123", "test")
    return db.cursor()


def test():
    cursor = start_connection()
    cursor.execute("SELECT * FROM test")
    data = cursor.fetchone()
    print ("Data : %s " % data)
    cursor.close()
    

test()
