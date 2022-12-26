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
from kivy.uix.screenmanager import FadeTransition,Screen
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout


####################  Kivymd imports ####################

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget, IconLeftWidgetWithoutTouch

#################### Other Imports ####################

import sys
import filetype
 


#################### imports from other Files ###########


# setting pathC:
sys.path.append('../Road-Damage-Detection') # neccessary for imports to be found 

from functions import *
from Mysql_functions import *
from run_yolo import run_rdd




#################### configuration / Global Variables

Window.maximize()








class Map(MapView):



    init = False
    damage_id_on_map_list = []
    damage_marker_list = []
    
    def load_points_from_db(self,*args):
            self.init = True
            #self.damage_id_on_map_list = []

            # if len(get_all_damages()) ==  0:

            #     app.root.screens[2].online = False


            for damage in get_all_damages():

                
                if damage.damage_id not in self.damage_id_on_map_list:
                    #self.damage_id_on_map_list.append(damage.damage_id)
                    marker = MapMarkerPopup(lat = damage.lat,lon = damage.lon,popup_size= (450,250))
                    
                    
                    butt = Button(text = "change",size= (130, 25),size_hint= (None, None))
                    if damage.timestamp != None:
                        date = damage.timestamp
                    else:
                        date = "unknown"
                    text = MDLabel(text = f"""Damage ID: {damage.damage_id}\nLocation: {round(damage.lat,3)}\\{round(damage.lon,3)}\nType: {damage.damageclass}\nSeverity: {damage.severity}\nWeather: {damage.weather}\nDate: {date.date()}\nTime: {date.time()}\nUser ID: {damage.user_id}\nRepair status: {damage.repair_status} """)

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
                    self.damage_marker_list.append((damage,marker))
                    self.damage_id_on_map_list.append(damage.damage_id)
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
        q = self.damage_marker_list
        for damage,marker in self.damage_marker_list:
            
            if damage.damageclass not in damage_filter.classselection:
                self.damage_id_on_map_list.remove(damage.damage_id)
                #self.damage_marker_list.remove((damage,marker))
                self.remove_widget(marker) 
                continue

            if damage.severity not in damage_filter.severityselection:
                self.damage_id_on_map_list.remove(damage.damage_id)
                #self.damage_marker_list.remove((damage,marker))
                self.remove_widget(marker)
                continue

            if damage.weather not in damage_filter.weatherselection:
                self.damage_id_on_map_list.remove(damage.damage_id)
                #self.damage_marker_list.remove((damage,marker))
                self.remove_widget(marker)
                continue

            if damage.user_id not in damage_filter.userselection and len(damage_filter.userselection) > 0:
                self.damage_id_on_map_list.remove(damage.damage_id)
                #self.damage_marker_list.remove((damage,marker))
                self.remove_widget(marker)
                continue

            if damage.repair_status not in damage_filter.repairstatusselection:
                self.damage_id_on_map_list.remove(damage.damage_id)
                #self.damage_marker_list.remove((damage,marker))
                self.remove_widget(marker)
                continue


            if len(damage_filter.areaselection) > 0:
                area = get_adress(damage.lat,damage.lon)
                for location in damage_filter.areaselection:
                    if location.lower() not in area.address.lower():
                   
                        self.damage_id_on_map_list.remove(damage.damage_id)
                        #self.damage_marker_list.remove((damage,marker))
                        self.remove_widget(marker)









        
            
class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()



###################### Classes for the filter selections menue ##################

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

####################### File selection pop class ################################################## 

class SaveFile(Popup):
    def Getthepath(self,filepath,app):
        
        app.root.screens[2].selected_path_list.append(str(filepath))

class Filepicker(GridLayout):
    
    def __init__(self, **kwargs):
        super(Filepicker, self).__init__(**kwargs)
        filepop = SaveFile()
        filepop.open()

############################# Screens #######################################

class Loginscreen(Screen):
    pass




class Mainscreen(Screen):
    
    filter_dropdown = ObjectProperty()
    damage_filter = Filter()
    online = True


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
            "viewclass": "MDRoundFlatIconButton",
            "text": "Apply Filter:",
            "icon": "filter",
            "on_release": lambda x="City": self.menu_callback(x),
            },
            # {
            # "viewclass": "MDProgressBar",
            # "id": "progress",
            # "type": "determinate",
            # "running_duration": "1",
            # "catching_duration": "1.5",
            # },

            
        ]
        self.filter_dropdown = MDDropdownMenu(
            width_mult = 8,
            caller=self.ids.filter_button,
            items=menu_items
            
            )

        


    def menu_callback(self,text_of_the_option):
        #self.repairstatusselection = repairstatusselection_good
        progressbar = None



        for filter in self.filter_dropdown.children[0].children[0].children[0].children:


            if filter.id == "areaselection":
                self.damage_filter.areaselection = []
                if len(filter.ids.areaselection.text) > 0:
                    all_areas = filter.ids.areaselection.text.split(",")
                    for area in all_areas:
                        self.damage_filter.areaselection.append(area)               
                print(self.damage_filter.areaselection)

            if filter.id == "severityselection":
                if filter.ids.severityselection_good.active:
                    self.damage_filter.severityselection.add(1)
                else:
                    self.damage_filter.severityselection.discard(1)
                if filter.ids.severityselection_medium.active:
                    self.damage_filter.severityselection.add(2)
                else:
                    self.damage_filter.severityselection.discard(2)
                if filter.ids.severityselection_bad.active:
                    self.damage_filter.severityselection.add(3)
                else:
                    self.damage_filter.severityselection.discard(3)
                print(self.damage_filter.severityselection)

            if filter.id == "classselection":
                if filter.ids.classselection_crack.active:
                    self.damage_filter.classselection.add('Crack')
                else:
                    self.damage_filter.classselection.discard('Crack')
                if filter.ids.classselection_allicrack.active:
                    self.damage_filter.classselection.add('Alligator Crack')
                else:
                    self.damage_filter.classselection.discard('Alligator Crack')
                if filter.ids.classselection_pothole.active:
                    self.damage_filter.classselection.add('Pothole')
                else:
                    self.damage_filter.classselection.discard('Pothole')
                print(self.damage_filter.classselection)

            if filter.id == "weatherselection":
                if filter.ids.weatherselection_good.active:
                    self.damage_filter.weatherselection.add(1)
                else:
                    self.damage_filter.weatherselection.discard(1)
                if filter.ids.weatherselection_bad.active:
                    self.damage_filter.weatherselection.add(0)
                else:
                    self.damage_filter.weatherselection.discard(0)
                print(self.damage_filter.weatherselection)
            
            if filter.id == "repairstatusselection":
                if filter.ids.repairstatusselection_good.active:
                    self.damage_filter.repairstatusselection.add(1)
                else:
                    self.damage_filter.repairstatusselection.discard(1)
                if filter.ids.repairstatusselection_bad.active:
                    self.damage_filter.repairstatusselection.add(0)
                else:
                    self.damage_filter.repairstatusselection.discard(0)
                print(self.damage_filter.repairstatusselection)

            if filter.id == "userselection":
                self.damage_filter.userselection = []
                if len(filter.ids.userselection.text) > 0:
                    all_users = filter.ids.userselection.text.split(",")
                    for user in all_users:
                        try:
                            user = int(user)
                            self.damage_filter.userselection.append(user)
                        except:
                            continue               
                print(self.damage_filter.userselection)

        self.ids.mapview.apply_filter(self.damage_filter)


class Settingsscreen(Screen):
    pass

class Complainscreen(Screen):
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

    def run_detection(self):
        if len(self.selected_path_list) > 0:
            for file in self.selected_path_list:
                run_rdd(file)



        



#################### Main App ####################

class MainApp(MDApp):
   

    def build(self):
        pass

##################### Functions for switching screens to make changes in animation etc. central

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

    def switch_to_Complainscreen(self):
        self.root.transition = FadeTransition(duration=0.5)
        self.root.current = "Complainscreen"

#############################################################################################################


    def reload_damages(self,mapview):
        mapview.print_points_from_db()

    def center_map(self,mapview,location):
        mapview.center(location)


    def callback2(self):
        return Filepicker()
    
    def callback3(self):
        pass


    

    
if __name__ == '__main__':
    MainApp().run()
