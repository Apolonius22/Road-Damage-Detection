#################### Info ####################




####################  Kivy imports ####################

from tkinter import E, Label
from kivy_garden.mapview import MapMarkerPopup,MapView
from kivy.properties import StringProperty, ObjectProperty
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
from kivymd.uix.menu import MDDropdownMenu


#################### configuration / Global Variables

Window.maximize()


#################### Other Imports ####################

import sys
 
# setting pathC:
sys.path.append('../Road-Damage-Detection')

from functions import *
from Mysql_functions import *


#################### Screens ####################


from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget, IconLeftWidgetWithoutTouch
import filetype

class Map(MapView):

    init = False
    damage_id_on_map_list = []
    
    def load_points_from_db(self,*args):
            self.init = True

            for damage in get_all_damages():

                
                if damage.damage_id not in self.damage_id_on_map_list:
                    #self.damage_id_on_map_list.append(damage.damage_id)
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
                    self.damage_id_on_map_list.append((damage,marker))
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


    def print_points_from_db(self):
        for damage in get_all_damages():
            print(damage)

    def apply_filter(self,damage_filter):
        self.load_points_from_db()
        for damage,marker in self.damage_id_on_map_list:
            
            if damage.damageclass not in damage_filter.classselection:
                self.remove_widget(marker)





        
            
class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class Areaselection(MDBoxLayout):
    pass
class Severityselection(MDBoxLayout):
    pass
class Classselection(MDBoxLayout):
    pass
class Weatherselection(MDBoxLayout):
    pass
class Userselection(MDBoxLayout):
    pass
class Repairstatusselection(MDBoxLayout):
    pass
    

class SaveFile(Popup):
    def Getthepath(self,filepath,app):
        
        app.root.screens[2].selected_path_list.append(str(filepath))




class Loginscreen(Screen):
    pass




class Mainscreen(Screen):
    
    filter_dropdown = ObjectProperty()
    damage_filter = Filter()


    def on_enter(self):
        menu_items = [
            {
            "viewclass": "MDLabel",
            "text": "Filter Damages:",
            #"icon": "language-python",
            #"on_release": lambda x="City": self.menu_callback(x),
            },
            {
            "viewclass": "Areaselection",
            "id": "areaselection",
            },
            {
            "viewclass": "Severityselection",
            "id": "severityselection",
            },
            {
            "viewclass": "Classselection",
            "id": "classselection",
            },
            {
            "viewclass": "Weatherselection",
            "id": "weatherselection",
            },
            {
            "viewclass": "Userselection",
            "id": "userselection",
            },
            {
            "viewclass": "Repairstatusselection",
            "good": "repairstatusselection_good.active",
            "id": "repairstatusselection",
            },
            {
            "viewclass": "MDIconButton",
            "text": "Apply Filter:",
            "icon": "language-python",
            "on_release": lambda x="City": self.menu_callback(x),
            },
        ]
        self.filter_dropdown = MDDropdownMenu(
            width_mult = 8,
            caller=self.ids.filter_button,
            items=menu_items
            
            )

        

    def menu_callback(self,text_of_the_option):
        #self.repairstatusselection = repairstatusselection_good

        for filter in self.filter_dropdown.children[0].children[0].children[0].children:

            if filter.id == "areaselection":
                self.damage_filter.areaselection = filter.ids.areaselection.text                
                print(self.damage_filter.areaselection)

            if filter.id == "severityselection":
                self.damage_filter.severityselection.update({"good":filter.ids.severityselection_good.active})
                self.damage_filter.severityselection.update({"medium":filter.ids.severityselection_medium.active})
                self.damage_filter.severityselection.update({"bad":filter.ids.severityselection_bad.active})
                print(self.damage_filter.severityselection)

            if filter.id == "classselection":
                if filter.ids.classselection_crack.active:
                    self.damage_filter.classselection.add('Crack')
                else:
                    self.damage_filter.classselection.discard('Crack')
                if filter.ids.classselection_allicrack.active:
                    self.damage_filter.classselection.add('AlligatorCrack')
                else:
                    self.damage_filter.classselection.discard('AlligatorCrack')
                if filter.ids.classselection_pothole.active:
                    self.damage_filter.classselection.add('Pothole')
                else:
                    self.damage_filter.classselection.discard('Pothole')
                print(self.damage_filter.classselection)


            if filter.id == "weatherselection":
                self.damage_filter.weatherselection.update({"good":filter.ids.weatherselection_good.active})
                self.damage_filter.weatherselection.update({"bad":filter.ids.weatherselection_bad.active})
                print(self.damage_filter.weatherselection)
            
            if filter.id == "repairstatusselection":
                self.damage_filter.repairstatusselection.update({"good":filter.ids.repairstatusselection_good.active})
                self.damage_filter.repairstatusselection.update({"bad":filter.ids.repairstatusselection_bad.active})
                print(self.damage_filter.repairstatusselection)

            if filter.id == "userselection":
                self.damage_filter.userselection = filter.ids.userselection.text                
                print(self.damage_filter.userselection)
        self.ids.mapview.apply_filter(self.damage_filter)

class Settingsscreen(Screen):
    pass

class Analyticsscreen(Screen):
    latestpath = ""
    selected_path_list = []

    def remove_path_from_list(self,test):
        #print(test)
        for i in self.ids.file_list.children:
            if i.id == test:
                self.selected_path_list.remove(test)
                self.ids.file_list.remove_widget(i)
        
        #self.ids.file_list.remove_widget(test)
        
    def add_path_to_list(self):
        try:
            kind = filetype.guess(self.selected_path_list[-1])
        except:
            self.selected_path_list.pop()
            return
        if kind.mime.startswith("video"):
            self.ids.file_list.add_widget(OneLineAvatarIconListItem(IconLeftWidgetWithoutTouch(icon="video"),IconRightWidget(icon="minus",on_release=lambda x: self.remove_path_from_list(str(self.selected_path_list[-1]))),id = str(self.selected_path_list[-1]),text = self.selected_path_list[-1]),len(self.ids.file_list.children)-1)
        else:
            self.selected_path_list.pop()


class Filepicker(GridLayout):
    
    def __init__(self, **kwargs):
        super(Filepicker, self).__init__(**kwargs)
        filepop = SaveFile()
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
        
    def switch_to_Loginscreen(self):
        self.root.transition = FadeTransition(duration=0.5)
        self.root.current = "Loginscreen"


    def reload_damages(self,mapview):
        mapview.print_points_from_db()

    def center_map(self,mapview,location):
        mapview.center(location)


    def callback2(self):#),instance):
        return Filepicker()
    
    def callback3(self):#),instance):
        pass


    

    
if __name__ == '__main__':
    MainApp().run()
