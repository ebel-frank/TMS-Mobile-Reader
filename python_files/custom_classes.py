from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import NoTransition
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.properties import (
    NumericProperty, 
    ColorProperty, 
    ListProperty, 
    ObjectProperty,
    StringProperty, 
    DictProperty)
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import MDList
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.list.list import IRightBodyTouch, IconLeftWidgetWithoutTouch, TwoLineAvatarIconListItem
from math import ceil, floor

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
        self.left_title_icon = MDIconButton(icon="account-circle", theme_text_color="Custom", text_color=self.color, pos_hint={"x": 0.5, "y": 0.1})
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
        self.right_title_icon = MDIconButton(icon="menu", theme_text_color="Custom", text_color=self.color, pos_hint={"x": 0.5, "y": 0.1})
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


class BottomNavWindow(MDBottomNavigation):

    add_tabs = ListProperty([])

    win_x_padding = NumericProperty(.96)

    win_y_padding = NumericProperty(.911)

    bg_color = ColorProperty([.9, .9, .9, 1])

    items_bg_color = ColorProperty([1, 1, 1, .5])

    items_div_color = ColorProperty([.9, .9, .9, 1])

    documents_list = ListProperty([])

    list_icon = StringProperty("dots-vertical")

    file_icon = StringProperty("file")

    current_tab = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tabs = []
        self.mdlist_obj = []
        self.icon_item_obj = []
        self.option_item_obj = []
        self.box2_list = []

    def on_add_tabs(self, *args):
        '''
        Initiate the Addition of the given navigation tabs on add_tabs specification.
        '''
        self._create_tabs()
        self.children[1].transition = NoTransition()
    def on_bg_color(self, *args):
        '''
        Updates the background color on bg_color specification
        '''
        tab = self.tabs[self.current_tab]
        tab.children[0].color_obj.rgba = self.bg_color
    
    def on_items_bg_color(self, *args):
        '''
        Updates the background color of the list items.
        '''
        tab = self.mdlist_obj[self.current_tab]
        for item in tab.children:
            item.bg_color = self.items_bg_color
        
    def on_current_tab(self, *args):
        self.scrollview_obj.current_tab = self.current_tab

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
        self.scrollview_obj.reset_list(self.current_tab)

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
        # add scrollview to box layout
        self.mdlist_obj.append(MDList(spacing=(dp(0), dp(5))))
        self.scrollview_obj = self.TMSScrollView()
        self.scrollview_obj.add_widget(self.mdlist_obj[-1])
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
        self._add_list_items()
        self.scrollview_obj.update_list_items(self.mdlist_obj[0])
        self.scrollview_obj.documents_list=self.documents_list
         
    def _add_list_items(self):
        '''
        function that adds the list items to the scrollview.
        '''
        tab_obj =  self.mdlist_obj[0]
        tab_list = self.documents_list[0][:10]
        for name,  day in tab_list:
            option_obj = self.OptionListItem(parent_class=self, icon = self.list_icon)
            icon_left_widget = IconLeftWidgetWithoutTouch(icon=self.file_icon)
            self.option_item_obj.append(option_obj)
            self.icon_item_obj.append(icon_left_widget)
            two_item_list = self.TwoItemList(parent_class=self, text=name, secondary_text=day)
            two_item_list.add_widget(icon_left_widget)
            two_item_list.add_widget(option_obj)
            tab_obj.add_widget(two_item_list)
    
    class TwoItemList(TwoLineAvatarIconListItem, TouchBehavior):
        def __init__(self, **kwargs) -> None:
            self.outter_class = kwargs['parent_class']
            kwargs.pop("parent_class")
            super().__init__(**kwargs)
        
        def on_long_touch(self, *args):
            self.outter_class.open_bottom_sheet()

    
    class OptionListItem(IRightBodyTouch, MDIconButton):
        adaptive_width = True
        def __init__(self, **kwargs) -> None:
            self.outter_class = kwargs['parent_class']
            kwargs.pop("parent_class")
            super().__init__(**kwargs)
        
        def on_release(self):
            self.outter_class.open_bottom_sheet()
            return super().on_release()


    class TMSScrollView(ScrollView):
        documents_list = ListProperty([])
        current_tab = NumericProperty(0)
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.effect_cls = "ScrollEffect"
            self.bar_width = 0
            self.bind(scroll_y=self.scroll_y_changed)
            self.documents_list_counts = []
            self.current_set_count = 1
            self.max_list_object = 10
            self.current_display_list = []
            self.list_objects = []
        
        def scroll_y_changed(self, *args):
            if self.scroll_y <= 0:
                max_num = ceil(self.documents_list_counts[self.current_tab]/self.max_list_object)
                if self.current_set_count < max_num:
                    self.current_set_count += 1
                    self.scroll_y = ((self.documents_list_counts[self.current_tab] % self.max_list_object)/(self.max_list_object-1)) * 0.99999 if self.current_set_count == max_num else 0.99999
                    self.rearrange_display_list()
            elif self.scroll_y >= 1:
                max_num = ceil(self.documents_list_counts[self.current_tab]/self.max_list_object)
                if self.current_set_count > 1:
                    self.current_set_count -= 1
                    self.scroll_y = 0.99999 - ((self.documents_list_counts[self.current_tab] % self.max_list_object)/(self.max_list_object-1)) if self.current_set_count == 1 else 0.00001  
                    self.rearrange_display_list()
                    
        def rearrange_display_list(self):
            li = self.documents_list[self.current_tab]
            last_num_selected = self.max_list_object * self.current_set_count
            floor_num = floor(self.documents_list_counts[self.current_tab]/self.max_list_object)
            if floor_num >= self.current_set_count:
                self.current_display_list = li[last_num_selected-self.max_list_object:last_num_selected]
            else:
                self.current_display_list = li[last_num_selected-self.max_list_object*2:][::-1][:self.max_list_object][::-1]
            self.update_list_items()
            
        def update_list_items(self, obj=None):
            if obj is None:
                for i in range(self.max_list_object):
                    self.list_objects[self.max_list_object-1-i].text = self.current_display_list[i][0]
                    self.list_objects[self.max_list_object-1-i].secondary_text = self.current_display_list[i][1]
            else:
                self.list_objects = obj.children

        def on_documents_list(self, *args):
            self.documents_list_counts = [len(i) for i in self.documents_list]
            self.reset_list(self.current_tab)
        
        def reset_list(self, current_tab):
            self.current_set_count = 1
            self.scroll_y = 1
            self.current_tab = current_tab
            self.rearrange_display_list()
if __name__ == "__main__":
    from kivymd.app import MDApp
    class Myapp(MDApp):
        def build(self):
            superBox = BoxLayout(orientation ='horizontal')
            
            btn3 = ToolBarTitle()
            
            superBox.add_widget(btn3)

            return superBox
    Myapp().run()