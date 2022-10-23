#################### Info ####################




####################  Kivy imports ####################

from tkinter import Label
from kivy_garden.mapview import MapMarkerPopup,MapView
from kivy.properties import StringProperty
from kivy.core.window import Window

####################  Kivy.uix imports ####################

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FadeTransition,Screen#, NoTransition, CardTransition, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout

####################  Kivymd imports ####################
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout

#################### configuration / Global Variables

Window.maximize()


#################### Other Imports ####################

from functions import *
from Mysql_functions import *


#################### Screens ####################



class Map(MapView):

    init = False
    damage_id_on_map_list = []
    
    def load_points_from_db(self,*args):
            self.init = True

            for damage in get_all_damages():

                
                if damage.damage_id not in self.damage_id_on_map_list:
                    self.damage_id_on_map_list.append(damage.damage_id)
                    marker = MapMarkerPopup(lat = damage.lat,lon = damage.lon,popup_size= (450,250))
                    
                    
                    butt = Button(text = "change",size= (130, 25),size_hint= (None, None))
                    if damage.timestamp != None:
                        date = damage.timestamp
                    else:
                        date = "unknown"
                    text = MDLabel(text = f"""Damage ID: {damage.damage_id}\nLocation: {damage.lat}\\{damage.lon}\nType: {damage.damageclass}\nSeverity: {damage.severity}\nWeather: {damage.weather}\nTimestamp: {date}\nUser ID: {damage.user_id}\nRepair status: {damage.repair_status} """)

                    first = BoxLayout(orientation = "horizontal",padding= "10dp",spacing=10)

                    card = MDCard(size_hint= (None, None),size= ("200dp", "220dp"))

                    second = BoxLayout(orientation = "vertical",padding= "10dp")



                    bub = Bubble(orientation = "horizontal")
                    img = Image(source = damage.piture_path, mipmap= True)

                    second.add_widget(text)
                    second.add_widget(butt)

                    card.add_widget(second)

                    first.add_widget(img)

                    first.add_widget(card)
                    bub.add_widget(first)
                    marker.add_widget(bub)

                    self.add_widget(marker)


    def init_damages(self,*args):
        if not self.init:
            lat = 49
            lon = 12
            
            self.center_on(lat, lon)
            self.load_points_from_db()
            print("initialize successfully")

    def center(self,location,*args):
        try:   
            if "," in location and isfloat(location.split(",")[0]) and isfloat(location.split(",")[1]):
                lat = float(location.split(",")[0])
                lon = float(location.split(",")[1])
                self.center_on(lat, lon)
                self.zoom = 13
            else:
                loc = Nominatim(user_agent="GetLoc")
                getLoc = loc.geocode(location)
                self.center_on(getLoc.latitude, getLoc.longitude)
                self.zoom = 13
        except:
            pass

        
            
class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class SaveFile(Popup):
    def Getthepath(self,filepath,lable):
        global Latestpath
        Latestpath=str(filepath)
        print("path",Latestpath)
        lable.text = Latestpath





class Mainscreen(Screen):
    pass

class Settingsscreen(Screen):
    pass

class Analyticsscreen(Screen):
    pass

class Filepicker(GridLayout):
    
    def __init__(self, lable, **kwargs):
        super(Filepicker, self).__init__(**kwargs)
        filepop = SaveFile(lable)
        filepop.open()
        



#################### Main App ####################

class MainApp(MDApp):
    


    def build(self):
        pass


    def switch_to_Analyticsscreen(self):
        self.root.transition = FadeTransition(duration=0.5)
        self.root.current = "Analyticsscreen"
        
    def switch_to_Mainscreen(self):
        self.root.transition = FadeTransition(duration=0.5)
        self.root.current = "Mainscreen"

    def switch_to_Settingsscreen(self):
        self.root.transition = FadeTransition(duration=0.5)
        self.root.current = "Settingsscreen"


    def reload_damages(self,mapview):
        mapview.load_points_from_db()

    def center_map(self,mapview,location):
        mapview.center(location)


    def callback2(self,lable):#),instance):
        global Latestpath
        return Filepicker(lable)

    
if __name__ == '__main__':
    MainApp().run()
