from database import *


def get_current_profile(username):
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'SELECT current_profile_id FROM User WHERE username="{0}"'.format(username)
    cursor.execute(sql)
    current_profile_id = cursor.fetchone()[0]

    sql = 'SELECT * FROM Profile WHERE profile_id={0}'.format(current_profile_id)
    cursor.execute(sql)
    profile = cursor.fetchone()

    conn.close()

    return profile

# ------------------------------------------------------------------------------

def add_profile(user_id, profile_name):
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'INSERT INTO Profile (user_id, name) VALUES ({0}, "{1}")'.format(user_id, profile_name)
    cursor.execute(sql)

    conn.commit()
    conn.close()
