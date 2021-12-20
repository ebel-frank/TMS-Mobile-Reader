
__version__ = "0.0.0"
# kivy imports
from kivy import require as kivyRequire
kivyRequire("2.0.0")
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager
# python imports
from threading import Thread
from time import sleep
# local imports
from python_files.files_path import FileDirectories
from python_files.classes import MainTabs
from python_files.custom_classes import ToolBarTitle, BottomNavWindow


class Manager(ScreenManager):
    pass


class MainManager(ScreenManager):
    pass


class TMSReaderApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "A700"

    def build(self):
        return Builder.load_file(FileDirectories.main_kv_file)
    
    def on_start(self):
        Thread(target=self.init_loading_sequence).start()
        return super().on_start()
    
    def init_loading_sequence(self):
        '''
        Loads all the kv and python widgets then links them to their parent widget.
        When all files are loaded and linked, it switches the screen to the loaded screen. 
        Run a seperate thread.
        '''
        ############################################################################################
        # Remove in Production
        sleep(1)
        ############################################################################################
        self.import_classes()
        self.load_kv_files()
        self.link_widgets()
        # Change to loaded screen
        self.root.current = "manager_screen"
    
    def import_classes(self):
        '''
        Dynamically imports python classes.
        '''
        #exec("from python_files.custom_classes import *")
        exec("from python_files.classes import LogIn")
        

    def load_kv_files(self):
        '''
        Builds other kv files not yet loaded (lazy build).
        '''
        #Builder.load_file(FileDirectories.custom_kv_file)
        Builder.load_file(FileDirectories.login_kv_file)
    
    def link_widgets(self):
        '''
        links all loaded objects (widgets) correctly
        '''
        # widgets_obj = Factory.MainTabs()
        # self.root.ids.manager.add_widget(widgets_obj)
        # self.root.ids.update(widgets_obj.ids)
        #
        widgets_obj = Factory.LogIn()
        self.root.ids.manager.add_widget(widgets_obj)
        self.root.ids.update(widgets_obj.ids)


if __name__ == '__main__':
    TMSReaderApp().run()
