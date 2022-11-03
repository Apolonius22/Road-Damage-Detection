import sqlite3
import os
from functions import Damage

path_to_db = os.path.dirname(__file__) + "\damageapp.sqlite"#r"C:\Users\tobia\Desktop\Studium\case_study_two\test\damageapp.sqlite"


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
    damagelist = []
    for i in bar_dict:
        damagelist.append(Damage(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
    return damagelist



# q = get_all_damages()
# for i in q:
#     print(i,"\n")


###################################################### online 


