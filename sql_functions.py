import sqlite3


path_to_db = r"C:\Users\tobia\Desktop\Studium\case_study_two\test\damageapp.sqlite"


def log_damage(lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status):
    conn = sqlite3.connect('damageapp.sqlite')
    cur = conn.cursor()
    cur.execute('''INSERT INTO damage (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ? )''' , (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status))
    conn.commit()
    conn.close()

def get_all_damages():
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    bar_cursor = cur.execute('SELECT * FROM damage')
    bar_dict = bar_cursor.fetchall()
    conn.close()
    return bar_dict

def getall():
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    bar_cursor = cur.execute('SELECT * FROM damage')
    bar_dict = bar_cursor.fetchall()
    conn.close()
    return bar_dict


#print(getall())