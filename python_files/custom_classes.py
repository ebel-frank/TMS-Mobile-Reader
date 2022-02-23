from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
#from kivy.uix.screenmanager import NoTransition
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.properties import (
    NumericProperty, 
    ColorProperty, 
    ListProperty, 
    StringProperty, 
    DictProperty)
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.list.list import IRightBodyTouch, IconLeftWidgetWithoutTouch, TwoLineAvatarIconListItem, OneLineListItem
from kivymd.uix.behaviors import TouchBehavior
from python_files.files_path import FileDirectories as FD
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivy.factory import Factory
from threading import Thread
from python_files.TMS_database import TMSDatabase
##########################################################################################################################

class MenuListItem(OneLineListItem):
    # This is an extension of the ListItem used in the Dropdown menu.
    # It tries to align the labels to the center which was previously more difficult
    # used in the app's menu
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.ids._lbl_primary.halign = "center"


class ToolBarTitle(BoxLayout):
    '''
    ToolBarTitle:
    
        A custom tool bar of the mobile application.

    PARAMETERS:

        pad_left: used to set the padding on the left side of the tool bar. param: (size:int) | default: 10

        pad_right: used to set the padding on the right side of the tool bar. param: (size:int) | default: 10

        color: used to set the color property of the tool bar. param: (r, g, b, a) | default: 1, 1, 1, 1

        bg_color: used to set the backgroud color of the tool bar. param: (r,g,b,a) | default: .2, .2, 1, 1

        halign_title: aligns the title in the specified direction. param: ('left', 'center', 'right') | default: "left"

        title_padding: used to set the padding on the left and right side of the title text. param: (numeric size:left, numeric size:right) | defualt: 20, 0

        text: used to set the title text. supports markup. param: ("Title") | default: "Title"

        bg_source: string directory to use for the background. param: ("source") | default: ""
        
        left_icon: string kivymd name or source to the left icon to use. param: ("icon name") | default: "account-circle"
        
        right_icon: string kivymd name or source to the right icon to use. param: ("icon name") | default: " menu"

        left_bind: Dictionary to the function to bind to the left icon. param: (Name = function) | default: None
        
        right_bind: Dictionary to the function to bind to the right icon. param: (Name = function) | default: None
        
        left_icon_size: size of the left icon to use. param: (w:int, h:int) | default: None, None
        
        right_icon_size: size of the right icon to use. param: (w:int, h:int) | default: None, None
        
    '''
    pad_left = NumericProperty(dp(10))

    pad_right = NumericProperty(dp(10))

    color = ColorProperty([1,1,1,1])

    bg_color = ColorProperty([.2,.2, 1,1])

    halign_title = StringProperty("left")

    title_padding = ListProperty([20,0])

    text = StringProperty("[b]Title[/b]")

    bg_source = StringProperty("")

    left_icon = StringProperty("")

    right_icon = StringProperty("")

    left_bind = DictProperty({})

    right_bind = DictProperty({})

    left_icon_size = ListProperty([])

    right_icon_Size = ListProperty([])

    md_font_style = ListProperty([])

    left_title_icon = MDIconButton(icon="account-circle", theme_text_color="Custom", text_color=(1,1,1,1), pos_hint={"x": 0.5, "y": 0.1})
    right_title_icon = MDIconButton(icon="menu", theme_text_color="Custom", text_color=(1,1,1,1), pos_hint={"x": 0.5, "y": 0.1})
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = 0.09
        self.pos_hint = {'top': 1}
        title_icon_menu = BoxLayout(orientation="horizontal")
        # Padding boxes (used for padding)
        self.left_box = BoxLayout(size_hint_x=None, width=self.pad_left)
        self.right_box = BoxLayout(size_hint_x=None, width=self.pad_right)
        # Icon
        icon = AnchorLayout(anchor_x='left', anchor_y='center')
        self.left_title_icon.bind(on_press=self.open_profile_page)
        icon.add_widget(self.left_title_icon)
        # Title
        title = BoxLayout(size_hint_x = 10)
        self.title_label = MDLabel(
            text= self.text, 
            theme_text_color="Custom", 
            text_color=self.color, 
            halign=self.halign_title,
            markup = True,
            padding=(self.title_padding[0], self.title_padding[1]))
        title.add_widget(self.title_label)
        # menu
        menu = AnchorLayout(anchor_x='right', anchor_y='center')
        self.right_title_icon.bind(on_press=self.open_title_menu)
        menu.add_widget(self.right_title_icon)
        # Add to main Layout
        title_icon_menu.add_widget(self.left_box)
        title_icon_menu.add_widget(icon)
        title_icon_menu.add_widget(title)
        title_icon_menu.add_widget(menu)
        title_icon_menu.add_widget(self.right_box)
        # Add to self layout
        self.add_widget(title_icon_menu)
        # Background
        with self.canvas.before:
            self.rect_color = Color(rgba=self.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.center)
        self.bind(pos= self.update_rect, size=self.update_rect)
        # Creating Menu attributes
        self.logged_in = False
        menu_names = ("About", "Settings", (lambda x: "Sign in" if not self.logged_in else "Sign out")(None))
        menu_items = [
            {
                "viewclass": "MenuListItem",
                "text": f'{name}',
                "on_release": lambda x= f'{name}': self.close_and_run_menu(x)
            } for name in menu_names
        ]
        self.menu = MDDropdownMenu(items=menu_items, width_mult=2, max_height=dp(145), radius=[dp(3)], opening_time=0)
    
    def open_title_menu(self, inst):
        '''
        called to open menu.
        '''
        self.menu.caller = inst
        self.menu.open()
    
    def open_profile_page(self, *args):
        '''
        Changes the display page to profile using the manager
        '''
        # self.parent.parent.transition.direction = 'down'
        # self.parent.parent.current = 'profile'
        Factory.ProfilePage().open()
    
    def close_and_run_menu(self, val):
        '''
        called to close menu and return to the signup page.
        '''
        self.menu.dismiss()
        if val == "Sign in" or val == "Sign out":
            # switch the window to the signup window
            self.parent.parent.transition.direction = 'left'
            self.parent.parent.current = 'login_signout'
            # manually focus the first text box of the signup window.
            #self.parent.parent.focus_signup()

    def update_rect(self, *args):
        '''
        updates the size and padding of the tool bar.
        '''
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.left_box.width = self.pad_left
        self.right_box.width = self.pad_right
    
    def on_pad_left(self, *args):
        '''
        updates the left padding of the tool bar when changed.
        '''
        self.left_box.width = self.pad_left

    def on_pad_right(self, *args):
        '''
        updates the right padding of the tool bar when changed.
        '''
        self.right_box.width = self.pad_right

    def on_color(self, *args):
        '''
        updates the text color of the tool bar when changed.
        '''
        self.title_label.text_color = self.left_title_icon.text_color = self.right_title_icon.text_color = self.color

    def on_bg_color(self, *args):
        '''
        updates the background color of the tool bar when changed.
        '''
        self.rect_color.rgba = self.bg_color

    def on_halign_title(self, *args):
        '''
        updates the horizontal alignment of the Title when  changed.
        '''
        self.title_label.halign = self.halign_title

    def on_title_padding(self, *args):
        '''
        updates the padding of the title label when changed.
        '''
        self.title_label.padding = (self.title_padding[0], self.title_padding[1])

    def on_text(self, *args):
        '''
        updates the text of the title when changed.
        '''
        self.title_label.text = self.text

    def on_bg_source(self, *args):
        '''
        updates the background texture with the source image.
        '''
        with self.canvas.before:
            self.rect_color.rgba = (1, 1, 1, 1)
            self.rect.source = self.bg_source
        
    def on_left_icon(self, *args):
        '''
        updates the left icon with the kivymd name or source icon.
        '''
        self.left_title_icon.icon = self.left_icon

    def on_right_icon(self, *args):
        '''
        updates the right icon with the kivymd name or source icon.
        '''
        self.right_title_icon.icon = self.right_icon
    
    def on_left_bind(self, *args):
        '''
        binds the left icon button with the parameter and function specified in the dictionary.
        '''
        self.left_title_icon.bind(**self.left_bind)

    def on_right_bind(self, *args):
        '''
        binds the right icon button with the parameter and function specified in the dictionary.
        '''
        self.right_title_icon.bind(**self.right_bind)

##############################################################################################################
##############################################################################################################

class OptionListItem(IRightBodyTouch, MDIconButton):
        adaptive_width = True
        def on_release(self):
            MDApp.get_running_app().open_bottom_sheet()
            


class LeftIcon(BoxLayout, IconLeftWidgetWithoutTouch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon=FD.file_icon
        #self.size_hint = (.2, .9)


class TwoItemList(TwoLineAvatarIconListItem, TouchBehavior):
    clicked_name = None
    is_long_touch = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)   
        self.left_icon_obj = LeftIcon()
        self.option_obj = OptionListItem(icon = "dots-vertical")
        self.add_widget(self.left_icon_obj)
        self.add_widget(self.option_obj)   

    def on_release(self):
        if not self.is_long_touch:
            ## code
            print(self.clicked_name)

        self.is_long_touch = False
    
    def on_long_touch(self, *args):
        self.is_long_touch = True
        MDApp.get_running_app().open_bottom_sheet()
        pass


    def called_by_parent(self, data:dict):
        '''
        function called by instance to update the document selected.
        '''
        self.clicked_name = data['text']
        
    
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, TwoItemList):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.called_by_parent(rv.data[index])
        

class RV(RecycleView):
    def __init__(self, data, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = data
        



class BottomNavWindow(MDBottomNavigation):

    add_tabs = ListProperty([])

    win_x_padding = NumericProperty(.96)

    win_y_padding = NumericProperty(.911)

    bg_color = ColorProperty([.9, .9, .9, 1])

    items_bg_color = ColorProperty([1, 1, 1, .5])

    items_div_color = ColorProperty([.9, .9, .9, 1])

    documents_list = ListProperty([])

    file_icon = StringProperty("file")

    current_tab = NumericProperty(0)

    local_database = TMSDatabase(FD.database_dir)

    # Load new files to database on start up.
    try:
        dirs = []
        for d in FD.search_dirs:
            dirs += FD.list_dirs(d)
        dir_names = list(set(dirs))
    except Exception as e:
        print("Search folder directory failed!", e)
    else:
        local_database.sync_db(dir_names)
        

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tabs = []
        self.mdlist_obj = []
        self.icon_item_obj = []
        self.option_item_obj = []
        self.box2_list = []
        Thread(target=self._search_dir).start() # should be multiprocessed

    def _search_dir(self, *args):
        try:
            Clock.schedule_once(lambda *x: self._refresh_list(0))
        except IndexError as e:
            print("document variable not yet created!", e,"\nExpected only once" )
    
    def _refresh_list(self, tab):
        '''
        updates the documents_list from the database.
        '''
        if tab == 0:
            self.documents_list[tab] = [{"text": i, "secondary_text": j} for i, j in self.local_database.get_file_name()]# testing
        # probably delete this guy (not well implemented)
            self.documents_list[1] = self.documents_list[0]+[{"text": i, "secondary_text": j} for i, j in self.local_database.get_file_name()]# testing

    def on_add_tabs(self, *args):
        '''
        Initiate the Addition of the given navigation tabs on add_tabs specification.
        '''
        self._create_tabs()
        #self.children[1].transition = NoTransition()

    def on_bg_color(self, *args):
        '''
        Updates the background color on bg_color specification
        '''
        tab = self.tabs[self.current_tab]
        tab.children[0].color_obj.rgba = self.bg_color        

    def on_file_icon(self, *args):
        '''
        Updates the file icon on the left to the specified one by file_icon.
        '''
        for item in self.icon_item_obj:
            item.icon = self.file_icon

    def on_list_icon(self, *args):
        '''
        Updates the file icon on the left to the specified one by file_icon.
        '''
        for item in self.option_item_obj:
            item.icon = self.list_icon
    
    def on_win_x_padding(self, *args):
        '''
        updates the horizontal width of the scrollable view.
        '''
        for box in self.box2_list:
            box.size_hint_x = self.win_x_padding
    
    def on_win_y_padding(self, *args):
        '''
        updates the vertical width of the scrollable view.
        '''
        for box in self.box2_list:
            box.size_hint_y = self.win_y_padding
    
    def _create_tabs(self):
        '''
        Creates the tabs bare body using the add_tabs and adds it as a widget.
        '''
        # create tab
        for tab_name, tab_text, tab_icon in self.add_tabs:
            tab = MDBottomNavigationItem(name=tab_name, text=tab_text, icon=tab_icon, on_tab_press=self.switch_to_tab)
            self.tabs.append(tab)
            self.add_widget(tab)
        self._tab_child = self._create_tab_child()
        self.tabs[0].add_widget(self._tab_child)

    def switch_to_tab(self, tab):
        self._tab_child.parent.remove_widget(self._tab_child)
        tab.add_widget(self._tab_child)
        self.current_tab = self.tabs.index(tab)
        self.scrollview_obj.data = self.documents_list[self.current_tab]
        
    def _create_tab_child(self):
        '''
        creates the scrollview and layout of the window and adds it to the parent bare body.
        '''
        self.box1 = RelativeLayout()
        box2 = BoxLayout(size_hint=(self.win_x_padding,self.win_y_padding), pos_hint={"center_x": 0.5, "bottom": 0}, on_size=self.update_boxlayout, on_pos=self.update_boxlayout)
        self.box2_list.append(box2)
        self.box1.bind(pos= self.update_boxlayout, size=self.update_boxlayout)
        with self.box1.canvas.before:
           self.box1.color_obj = Color(rgba=self.bg_color)
           self.box1.rect_obj = Rectangle(size=self.box1.size, pos=self.box1.size)
        self.scrollview_obj = RV([])
        box2.add_widget(self.scrollview_obj)
        self.box1.add_widget(box2)
        return self.box1
    
    def update_boxlayout(self, *args):
        '''
        function to be called by the background widget to update the background size.
        '''
        args[0].rect_obj.size = args[0].size
        args[0].rect_obj.pos = args[0].pos
    
    def on_documents_list(self, *args):
        '''
        Initiate the Addition of the given list item of the corresponding documents specified.
        '''
        try:
            self.scrollview_obj.data = self.documents_list[self.current_tab]
        except AttributeError as e:
            print("Scroll View (Recycle View) not yet created!", e,"\nExpected only once" )
        FD()

        
    
  ##############################################################################################################      
         
