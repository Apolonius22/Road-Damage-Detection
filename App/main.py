from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFillRoundFlatButton,MDRectangleFlatButton
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.popup import PopupException
from kivy.factory import Factory
from kivymd.uix.dialog import MDDialog
from kivy.config import Config
from kivy.metrics import dp,sp
from kivy.app import runTouchApp
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
import cv2
import numpy
from kivy import platform

if platform == "android":
     from android.permissions import request_permissions, Permission
     from android.storage import primary_external_storage_path
     request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET,Permission.ACCESS_WIFI_STATE,Permission.CAMERA])


from Mysql_functions import *

#Building the App
class main(MDApp):
    def __init__(self, **kwargs):
        self.title = "Road Damages"
        super().__init__(**kwargs)

    def build(self):
        sm=ScreenManager()
        sm.add_widget(StartScreen(name='StartScreen'))
        sm.add_widget(SignIn(name='SignIn'))
        sm.add_widget(MainScreen(name='MainScreen'))
        sm.add_widget(SignUp(name='SignUp'))    
        sm.add_widget(PolicyandTerms(name='PolicyandTerms'))
        sm.add_widget(ImageCaptions(name='ImageCaptions'))
        sm.add_widget(Complain(name='Complain'))
        sm.add_widget(NewComplaint(name='NewComplaint'))
        sm.add_widget(NewComplaint(name='NewComplaint'))

        window_sizes=Window.size
        print("the window size is", window_sizes)
        #Window.size = (1080, 2042)
        self.icon="applogo.png"
        #Config.set('graphics', 'width', '480')
        #Config.set('graphics', 'height', '800')

        return Builder.load_file('main2.kv')

class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass 
class ImageCaptions(Screen):
    pass 
class SignIn(Screen):
    pass 
class UnderConstruction(Screen):
    pass 

class SignUp(Screen):
    def Genderdisplay_dropdown(self):
        self.menu = MDDropdownMenu(
            caller=self.ids.gender,
            items=[{"viewclass": "OneLineListItem", "text": "Male","on_release":lambda x="Male":self.male()},{"viewclass": "OneLineListItem", "text": "Female","on_release":lambda x="Female":self.female()}],
            position="bottom",
            width_mult=2,
        )
        self.menu.open()
    def male(self):
        self.ids.gender.text="Male"
    def female(self):
        self.ids.gender.text="Female"

    def Empdisplay_dropdown(self):
        self.menu = MDDropdownMenu(
            caller=self.ids.employment_Status,
            items=[{"viewclass": "OneLineListItem", "text": "Full time","on_release":lambda x="Full time":self.FullTime()},
            {"viewclass": "OneLineListItem", "text": "Part time","on_release":lambda x="Part time":self.PartTime()},
            {"viewclass": "OneLineListItem", "text": "Student","on_release":lambda x="Student":self.Student()},
            {"viewclass": "OneLineListItem", "text": "Retired","on_release":lambda x="Retired":self.Retired()}],
            position="bottom",
            width_mult=10,
        )
        self.menu.open()
    def FullTime(self):
        self.ids.employment_Status.text="Full time"
    def PartTime(self):
        self.ids.employment_Status.text="Part time"
    def Student(self):
        self.ids.employment_Status.text="Student"
    def Retired(self):
        self.ids.employment_Status.text="Retired"

    def CollectDate(self):
        global Username
        Username= self.ids.username.text
        global UserPassword
        UserPassword=self.ids.password.text
        global UserBirthday
        UserBirthday=self.ids.birthday.text
        global UserGender
        UserGender=self.ids.gender.text
        global UserResidence
        UserResidence=self.ids.residence.text
        global UserEmpStatus
        UserEmpStatus=self.ids.employment_Status.text
        print(Username)
        UserNameCon=CheckUserName(Username)
        if UserNameCon:
            self.manager.current="PolicyandTerms"
            self.manager.transition.direction="left"
            UserNameCon=True

class PolicyandTerms(Screen):
    def checkbox_click(self,instanse,value):
        if value==False:
            self.ids.ConfirmB.disabled=True
        else:
            self.ids.ConfirmB.disabled=False
    def RegisterInfo(self):
        total_gained_points=int(0)
        UserRegistration(Username,UserPassword,UserBirthday,UserGender,UserResidence,UserEmpStatus,total_gained_points)
class MainScreen(Screen):
    pass 

class Setting(Screen):
    pass  
class Complain(Screen):
    pass 
class NewComplaint(Screen):
    def Compl_Selection(self):
        self.menu = MDDropdownMenu(
            caller=self.ids.Complaint_type,
            items=[{"viewclass": "OneLineListItem", "text": "Cycle-sidewalk damages","on_release":lambda x="Cycle-sidewalk damages":self.option1()},
            {"viewclass": "OneLineListItem", "text": "obstacles","on_release":lambda x="obstacles":self.option2()},
            {"viewclass": "OneLineListItem", "text": "Malfunction traffic lights","on_release":lambda x="Malfunction traffic lights":self.option3()},
            {"viewclass": "OneLineListItem", "text": "Damaged traffic signs","on_release":lambda x="Damaged traffic signs":self.option4()}],
            position="bottom",
            width_mult=10,
        ) 
        self.menu.open()
    def option1(self):
        self.ids.Complaint_type.text="Cycle-sidewalk damages"
    def option2(self):
        self.ids.Complaint_type.text="obstacles"
    def option3(self):
        self.ids.Complaint_type.text="Malfunction traffic lights"
    def option4(self):
        self.ids.Complaint_type.text="Damaged traffic signs"
class ContactUs(Screen):
    pass 

if __name__=="__main__":
        Config.set('graphics', 'fullscreen', 'auto')
        Config.set('graphics', 'window_state', 'maximized')
        main().run()