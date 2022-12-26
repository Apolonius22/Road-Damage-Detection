from enum import unique
import sqlite3
import os
from functions import *
import mysql.connector
from mysql.connector import errorcode
from kivy.uix.popup import Popup
from kivy.uix.label import Label


#mydb = mysql.connector.connect(
#  host="sql11.freesqldatabase.com",
#  user="sql11528243",
#  password="fEPPIBNUJ8",
#  database="sql11528243"
#)

config = {
  'host':'roaddamages2.mysql.database.azure.com',
  'user':'CaseStudyMSS2',
  'password':'BestTeam123',
  'database':'roaddamages',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': r'C:\Users\tobia\Documents\GitHub\Road-Damage-Detection\DigiCertGlobalRootG2.crt.pem'
}


def get_cursor():
    try:
       mydb = mysql.connector.connect(**config)
       print("Connection established")
    except mysql.connector.Error as err:
        mydb = None
        mycursor = None
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        mycursor = mydb.cursor()

    return mycursor, mydb



                                                        #YYYY-MM-DD HH-MM-SS###########
def log_damage(lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status,image):
    mycursor, mydb = get_cursor()
    if mycursor != None or mydb != None: 

        previous_damages = get_all_damages()
        damage_unique = True
        for damage in previous_damages:
            if damage.lat == lat and damage.lon == lon:# and damage.damageclass == damageclass:
                damage_unique = False
        if damage_unique:
            #mycursor = mydb.cursor()
            sql = '''INSERT INTO registered_damages (lat, lon, damage_class, severity_class, weather, timestamp, user_id, repair_status,image) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            val = (lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status,image)
            mycursor.execute(sql, val)
            mydb.commit()
            print("logged successfully")
        else:
            print("damage GPS already logged")
        mycursor.close()
        mydb.close()

def log_damage(Damage):
    mycursor, mydb = get_cursor()
    if mycursor != None or mydb != None: 

        previous_damages = get_all_damages()
        damage_unique = True
        for damage in previous_damages:
            if damage.lat == Damage.lat and damage.lon == Damage.lon:# and damage.damageclass == damageclass:
                damage_unique = False
        if damage_unique:
            #mycursor = mydb.cursor()
            sql = '''INSERT INTO registered_damages (lat, lon, damage_class, severity_class, weather, timestamp, user_id, repair_status,image) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            val = (Damage.lat, Damage.lon, Damage.damageclass, Damage.severity, Damage.weather, Damage.timestamp, Damage.user_id, Damage.repair_status, Damage.piture_path)
            mycursor.execute(sql, val)
            mydb.commit()
            print("logged successfully")
        else:
            print("damage GPS already logged")
        mycursor.close()
        mydb.close()


def get_all_damages():
    mycursor, mydb = get_cursor()
    damagelist = []
    if mycursor != None or mydb != None:
        mycursor.execute("SELECT * FROM registered_damages")
        myresult = mycursor.fetchall()
        
        for i in myresult:
            picture_storing_path = current_path +f"\\cache\\{i[0]}.jpg"
            #write_file(i[9], storing_path)
            damagelist.append(Damage(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],picture_storing_path))
        mycursor.close()
        mydb.close()
        
    return damagelist



def log_user(email, password, points):
    mycursor, mydb = get_cursor()
    if mycursor != None or mydb != None:
        sql = "INSERT INTO Users (email, password, points) VALUES (%s, %s, %s)"
        val = (email, password, points)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        print("logged successfully")


def get_all_users():
    
    mycursor, mydb = get_cursor()
    
    if mycursor != None or mydb != None:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Users")
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return myresult
    else:
        return []

###################################################################

def CheckUserName(user_name):
    
    mycursor, mydb = get_cursor()
    if mycursor != None or mydb != None:
        mycursor.execute('SELECT * FROM users WHERE user_name = %(username)s',{'username' : user_name})
        checkUsername = mycursor.fetchall()
        User_unique=True
        print(checkUsername)
        if len(checkUsername) !=0 :
            print("User Name exists")
            pop = Popup(title='Invalid Username', title_align = 'center',
                        content=Label(text='The username is already taken.\nPlease try another one'),
                        size_hint=(0.8, 0.3), size=(1,1),
                        )
            pop.open()
            User_unique=False
            mycursor.close()
            mydb.close()
        print("checked successfully")
        return User_unique

def UserRegistration(user_name, password, birthday, gender, residence, employment_status,total_gained_points):
    
    mycursor, mydb = get_cursor()
    if mycursor != None or mydb != None:
        sql="INSERT INTO users (user_name, password, birthday, gender, residence, employment_status,total_gained_points) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        val=(user_name, password, birthday, gender, residence, employment_status,total_gained_points)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Successfully registered")
        mycursor.close()
        mydb.close()
        print("logged successfully")



############### debugging code ##############
if False: 
###############################################YYYY-MM-DD HH-MM-SS###########
#              lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status,image
    log_damage(49.221039, 12.675019, 3, 2, 0, "2022-11-23 12:01:11", 2, 0,"Test")
    #print(CheckUserName("hans"))
    #for damage in get_all_damages():
    #            print(damage)
    #print(get_all_users())