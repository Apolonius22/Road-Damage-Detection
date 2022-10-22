from enum import unique
import sqlite3
import os
from functions import *
import mysql.connector


path_to_db = os.path.dirname(__file__) + "\damageapp.sqlite"#r"C:\Users\tobia\Desktop\Studium\case_study_two\test\damageapp.sqlite"


def log_damage(lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status,path):
    previous_damages = get_all_damages()
    damage_unique = True
    for damage in previous_damages:
        if damage.lat == lat and damage.lon == lon:# and damage.damageclass == damageclass:
            damage_unique = False
    if damage_unique:
        mycursor = mydb.cursor()
        sql = '''INSERT INTO Damage (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status,picture) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        binary_picture = convertToBinaryData(path)
        val = (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status,binary_picture)
        mycursor.execute(sql, val)
        mydb.commit()
        print("logged successfully")
    else:
        print("damage GPS already logged")

def get_all_damages():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Damage")
    myresult = mycursor.fetchall()
    damagelist = []
    for i in myresult:
        storing_path = current_path +f"\\cache\\{i[0]}.jpg"
        write_file(i[9], storing_path)
        damagelist.append(Damage(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],storing_path))
    return damagelist

########## #online MSQL ####################

mydb = mysql.connector.connect(
  host="sql11.freesqldatabase.com",
  user="sql11528243",
  password="fEPPIBNUJ8",
  database="sql11528243"
)

def log_damage(lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status):
    previous_damages = get_all_damages()
    damage_unique = True
    for damage in previous_damages:
        if damage.lat == lat and damage.lon == lon:# and damage.damageclass == damageclass:
            damage_unique = False
    if damage_unique:
        mycursor = mydb.cursor()
        sql = '''INSERT INTO Damage (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
        val = (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status)
        mycursor.execute(sql, val)
        mydb.commit()
        print("logged successfully")
    else:
        print("damage GPS already logged")


def get_all_damages():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Damage")
    myresult = mycursor.fetchall()
    damagelist = []
    for i in myresult:
        storing_path = current_path +f"\\cache\\{i[0]}.jpg"
        write_file(i[9], storing_path)
        damagelist.append(Damage(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],storing_path))
    return damagelist



def log_user(email, password, points):

    mycursor = mydb.cursor()
    sql = "INSERT INTO Users (email, password, points) VALUES (%s, %s, %s)"
    val = (email, password, points)
    mycursor.execute(sql, val)
    mydb.commit()


def get_all_users():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Users")
    myresult = mycursor.fetchall()
    return myresult
