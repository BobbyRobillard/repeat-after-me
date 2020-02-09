from database import *


def get_current_profile(username):
    cursor = start_connection()

    sql = 'SELECT current_profile_id FROM User WHERE username="{0}"'.format(username)
    cursor.execute(sql)
    current_profile_id = cursor.fetchone()[0]

    sql = 'SELECT * FROM Profile WHERE profile_id={0}'.format(current_profile_id)
    cursor.execute(sql)
    profile = cursor.fetchone()

    cursor.close()

    return profile
