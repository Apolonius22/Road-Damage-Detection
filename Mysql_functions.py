import sqlite3
import os
from functions import Damage
import mysql.connector


path_to_db = os.path.dirname(__file__) + "\damageapp.sqlite"#r"C:\Users\tobia\Desktop\Studium\case_study_two\test\damageapp.sqlite"


def log_damage_local(lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status):
    conn = sqlite3.connect('damageapp.sqlite')
    cur = conn.cursor()
    cur.execute('''INSERT INTO damage (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ? )''' , (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status))
    conn.commit()
    conn.close()

def get_all_damages_local():
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


########## #online MSQL ####################


mydb = mysql.connector.connect(
  host="sql11.freesqldatabase.com",
  user="sql11528243",
  password="fEPPIBNUJ8",
  database="sql11528243"
)



def log_user(email, password, points):

    mycursor = mydb.cursor()
    sql = "INSERT INTO Users (email, password, points) VALUES (%s, %s, %s)"
    val = (email, password, points)
    mycursor.execute(sql, val)
    mydb.commit()


def log_damage(lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status):
    
    mycursor = mydb.cursor()
    sql = '''INSERT INTO Damage (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    val = (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status)
    mycursor.execute(sql, val)
    mydb.commit()
    print("logged successfully")

def get_all_damages():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Damage")
    myresult = mycursor.fetchall()
    damagelist = []
    for i in myresult:
        damagelist.append(Damage(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
    return damagelist


#log_damage(12.5,12.5,1,1,1,"2020-10-31 10:30:22",22,1)
#for i in get_all_damages():
#    print(i)