from database import *
# ------------------------------------------------------------------------------


def get_user_id():
    return 1


# ------------------------------------------------------------------------------


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


def add_profile(profile_name):
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'INSERT INTO Profile (user_id, name) VALUES ({0}, "{1}")'.format(
        get_user_id(),
        profile_name
    )
    cursor.execute(sql)

    conn.commit()
    conn.close()

# ------------------------------------------------------------------------------


def get_profiles(user_id):
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'SELECT Name FROM Profile WHERE user_id={0}'.format(user_id)
    cursor.execute(sql)

    names = [result[0] for result in cursor]

    conn.close()

    concated_profile_names = ""

    for name in names:
        concated_profile_names = concated_profile_names + (name + "\n")

    return concated_profile_names


# ------------------------------------------------------------------------------


def set_current_profile(profile_id):
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'UPDATE User SET current_profile_id={1} WHERE user_id={0}'.format(get_user_id(), profile_id)
    cursor.execute(sql)

    conn.commit()
    conn.close()
