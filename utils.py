from database import *

is_recording = False
curr_recording_actions = []

# ------------------------------------------------------------------------------
# User Methods
# ------------------------------------------------------------------------------
def get_user_id():
    return 1
# ------------------------------------------------------------------------------
def set_recording_key(new_key_code):
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'UPDATE User SET recording_key="{0}" WHERE user_id={1}'.format(new_key_code, get_user_id())
    cursor.execute(sql)

    conn.commit()
    conn.close()
# ------------------------------------------------------------------------------
def get_recording_key():
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'SELECT recording_key FROM User WHERE user_id={0}'.format(get_user_id())
    cursor.execute(sql)
    recording_key = cursor.fetchone()[0]
    conn.close()

    return recording_key
# ------------------------------------------------------------------------------
def set_active_mode_key(new_key_code):
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'UPDATE User SET active_mode_key="{0}" WHERE user_id={1}'.format(new_key_code, get_user_id())
    cursor.execute(sql)

    conn.commit()
    conn.close()
# ------------------------------------------------------------------------------
def get_active_mode_key():
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'SELECT active_mode_key FROM User WHERE user_id={0}'.format(get_user_id())
    cursor.execute(sql)
    recording_key = cursor.fetchone()[0]
    conn.close()

    return recording_key
# ------------------------------------------------------------------------------
def set_play_mode_key(new_key_code):
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'UPDATE User SET play_mode_key="{0}" WHERE user_id={1}'.format(new_key_code, get_user_id())
    cursor.execute(sql)

    conn.commit()
    conn.close()
# ------------------------------------------------------------------------------
def get_play_mode_key():
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'SELECT play_mode_key FROM User WHERE user_id={0}'.format(get_user_id())
    cursor.execute(sql)
    recording_key = cursor.fetchone()[0]
    conn.close()

    return recording_key
# ------------------------------------------------------------------------------
# Profile Methods
# ------------------------------------------------------------------------------
def get_current_profile():
    conn = start_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = 'SELECT current_profile_id FROM User WHERE user_id={0}'.format(get_user_id())
    cursor.execute(sql)
    current_profile_id = cursor.fetchone()['current_profile_id']

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
def get_profiles():
    conn = start_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = 'SELECT * FROM Profile WHERE user_id={0}'.format(get_user_id())
    cursor.execute(sql)

    profiles = [result for result in cursor]

    for profile in profiles:
        print(str(profile))

    conn.close()

    return profiles
# ------------------------------------------------------------------------------
def set_current_profile(profile_id):
    conn = start_connection()
    cursor = conn.cursor()

    sql = 'UPDATE User SET current_profile_id={1} WHERE user_id={0}'.format(get_user_id(), profile_id)
    cursor.execute(sql)

    conn.commit()
    conn.close()
# ------------------------------------------------------------------------------
# Recording Methods
# ------------------------------------------------------------------------------
def start_recording():
    global is_recording
    is_recording = True
# ------------------------------------------------------------------------------
def stop_recording():
    global is_recording
    is_recording = False
    # save_recording(curr_recording_actions)
