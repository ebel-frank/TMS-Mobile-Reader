
__version__ = "0.2"
# kivy imports
from kivy import require as kivyRequire
kivyRequire("2.0.0")
from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.weakproxy import WeakProxy
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.bottomsheet import MDListBottomSheet
# python imports
from threading import Thread
# local imports
from python_files.files_path import FileDirectories


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
        self.import_classes()
        self.load_kv_files()
        Clock.schedule_once(lambda x: self.link_widgets())
        # Change to loaded screen
        self.root.current = "manager_screen"
    
    def import_classes(self):
        '''
        Dynamically imports python classes.
        '''
        exec("from python_files.custom_classes import *")
        exec("from python_files.classes import *")
        

    def load_kv_files(self):
        '''
        Builds other kv files not yet loaded (lazy build).
        '''
        Builder.load_file(FileDirectories.manager_kv_file)
        Builder.load_file(FileDirectories.login_kv_file)
        Builder.load_file(FileDirectories.custom_kv_file)
        Builder.load_file(FileDirectories.profile_file)
    
    def link_widgets(self):
        '''
        links all loaded objects (widgets) correctly
        '''
        widgets_obj = Factory.Manager()
        self.root.ids.manager_screen.add_widget(widgets_obj)
        self.root.ids.update({"manager":WeakProxy(widgets_obj)})
        # self.root.ids.manager.add_widget(widgets_obj)
        # self.root.ids.update(widgets_obj.ids)
        #
        # widgets_obj = Factory.LogIn()
        # self.root.ids.manager.add_widget(widgets_obj)
        # self.root.ids.update(widgets_obj.ids)

    def open_bottom_sheet(self):
        '''
        opens the bottom drawer.
        '''
        # try:
        #     self.btmshtobj.dismiss(force=True)
        # except:
        #     pass
        try:
            if not self.btmshtobj_opened:
                self.btmshtobj_opened = True
                self.btmshtobj = MDListBottomSheet(duration_opening=0, radius=15, radius_from="top")
                self.btmshtobj.add_item('Add to favourite', lambda x: self.add2favourite(), 'star')
                self.btmshtobj.add_item('Delete file', lambda x: self.delete_file(), 'delete')
                self.btmshtobj.add_item('Move file', lambda x: self.move_file(), 'folder-move')
                self.btmshtobj.add_item('Rename file', lambda x: self.rename_file(), 'rename-box')
                # self.btmshtobj.add_item('Share file', lambda x: self.share_file(), 'file-send')
                # self.btmshtobj.add_item('Download audio', lambda x: self.download_audio(), 'download')
                self.btmshtobj.open()
        except:
            self.btmshtobj_opened = False
            if not self.btmshtobj_opened:
                self.btmshtobj_opened = True
                self.btmshtobj = MDListBottomSheet(duration_opening=0, radius=20, radius_from="top")
                self.btmshtobj.add_item('Add to favourite', lambda x: self.add2favourite(), 'star')
                self.btmshtobj.add_item('Delete file', lambda x: self.delete_file(), 'delete')
                self.btmshtobj.add_item('Move file', lambda x: self.move_file(), 'folder-move')
                self.btmshtobj.add_item('Rename file', lambda x: self.rename_file(), 'rename-box')
                # self.btmshtobj.add_item('Share file', lambda x: self.share_file(), 'file-send')
                # self.btmshtobj.add_item('Download audio', lambda x: self.download_audio(), 'download')
                self.btmshtobj.open()
        finally:
            self.btmshtobj_opened = False
        
    
    def add2favourite(self):
        pass

    def delete_file(self):
        pass

    def move_file(self):
        pass

    def rename_file(self):
        pass

    # def share_file(self):
    #     pass
    # def download_audio(self):
    #     pass

if __name__ == '__main__':
    TMSReaderApp().run()
