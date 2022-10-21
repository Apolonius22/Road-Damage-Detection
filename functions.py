from geopy.geocoders import Nominatim

class Damage:
    def __init__(self,damage_id, lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status):

        damagetypelist=['Pothole','Crack','AlligatorCrack'] 


        self.damage_id = damage_id
        self.lat = lat
        self.lon = lon
        self.damageclass = damagetypelist[damageclass]
        self.severity = severity
        self.weather = weather
        self.timestamp = timestamp
        self.user_id = user_id
        self.repair_status = repair_status

    def __str__(self):
        return f"Damage_ID:{self.damage_id}\nGPS:{self.lat}\\{self.lon}\nClass:{self.damageclass}\nSeverity:{self.severity}\nWeather:{self.weather}\nTimestamp:{self.timestamp}\nUser_id:{self.user_id}\nRepair_status:{self.repair_status}"



def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def get_adress(Latitude,Longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(Latitude+","+Longitude)

    return location