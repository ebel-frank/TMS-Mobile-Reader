from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock


class Manager(ScreenManager):
    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda *x: self._run_once(), 1)
        return super().on_kv_post(base_widget)
    
    def _run_once(self):
        self.ids.floating_btn.opacity = 1


class MainTabs(Screen):
    pass


class LogIn(Screen):
    pass


class Profile(Screen):
    pass


