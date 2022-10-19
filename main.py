#################### Info ####################




#################### imports ####################

from cProfile import run
from kivy.app import App
from kivy_garden.mapview import MapMarkerPopup,MapView
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, NoTransition, CardTransition, ScreenManager
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from sql_functions import get_all_damages
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.properties import ObjectProperty
#from kivymd.uix.textfield import MDTextFieldRound


#################### configuration
from kivymd.app import MDApp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.card import MDCardSwipe
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.bubble import Bubble
from kivy.uix.image import Image
from kivy.uix.screenmanager import FadeTransition

Window.maximize()
damagetypelist=['Pothole','Crack','AlligatorCrack'] 




from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty

from kivymd.uix.button import MDRectangleFlatIconButton


from kivy.uix.popup import Popup

from geopy.geocoders import Nominatim


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

#################### Screens ####################



class Map(MapView):

    init = False
    
    def load_points_from_db(self,*args):
            self.init= True
            damagelist = get_all_damages()

            for damage in damagelist:
                marker = MapMarkerPopup(lat = damage[1],lon = damage[2],popup_size= (450,250))
                
                
                
                
                butt = Button(text = "change",size= (130, 25),size_hint= (None, None))
                if damage[6] != None:
                    date = f"{damage[6][8:10]}:{damage[6][5:7]}:{damage[6][0:4]}"
                else:
                    date = "unknown"
                text = MDLabel(text = f"""Damage ID: {damage[0]}\nLocation: {damage[1]}\\{damage[2]}\nType: {damagetypelist[damage[3]]}\nSeverity: {damage[4]}\nWeather: {damage[5]}\nTimestamp: {date}\nUser ID: {damage[7]}\nRepair status: {damage[8]} """)

                first = BoxLayout(orientation = "horizontal",padding= "10dp",spacing=10)
                
                card = MDCard(    size_hint= (None, None),size= ("200dp", "220dp"))
                
                second = BoxLayout(orientation = "vertical",padding= "10dp")




                
                
                bub = Bubble(orientation = "horizontal")
                img = Image(source= '1.jpg',mipmap= True)
                
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
            self.load_points_from_db()

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
    def Getthepath(self,filepath):
        global Latestpath
        Latestpath=str(filepath)
        print("path",Latestpath)





class Mainscreen(Screen):
    pass
class Settingsscreen(Screen):
    pass

class Analyticsscreen(Screen):
    pass



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


        
    
if __name__ == '__main__':
    MainApp().run()
