
__version__ = "0.0.0"
# kivymd imports
from kivymd.app import MDApp
# kivy imports
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager
# python imports
from multiprocessing import Process, set_start_method
# local imports
from python_files.files_path import FileDirectories


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
        print(platform)
        if platform == "win":
            set_start_method("spawn")
        Process(target=self.init_loading_sequence).start()
        return super().on_start()
    
    def init_loading_sequence(self):
        self.import_classes()
        self.load_kv_files()
        self.link_widgets()
        # Change to loaded screen
        self.root.current = "manager_screen"
    
    def import_classes(self):
        exec("from python_files.classes import *")

    def load_kv_files(self):
        Builder.load_file(FileDirectories.maintabs_kv_file)
    
    def link_widgets(self):
        self.root.ids.manager.add_widget(Factory.MainTabs())
        self.root.ids.manager.add_widget(Factory.LogIn())

if __name__ == '__main__':
    TMSReaderApp().run()
