from pathlib import Path
from kivy.utils import platform

if platform == "android":
    from android.runnable import run_on_ui_thread
    from android.storage import primary_external_storage_path
    from android.permissions import request_permissions, Permission
    from jnius import autoclass

    Color = autoclass("android.graphics.Color")
    WindowManager = autoclass('android.view.WindowManager$LayoutParams')
    activity = autoclass('org.kivy.android.PythonActivity').mActivity


class FileDirectories:
    if platform == "android":

        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

        @run_on_ui_thread
        def statusbar(self, topcolor, btmcolor):
            window = activity.getWindow()
            window.clearFlags(WindowManager.FLAG_TRANSLUCENT_STATUS)
            window.addFlags(WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
            window.setStatusBarColor(Color.parseColor(topcolor)) 
            window.setNavigationBarColor(Color.parseColor(btmcolor))
        
        primary_ext_storage = primary_external_storage_path()
        app_home = str(Path.cwd()) 
        android_home = str(Path.cwd().parents[1])

        top_nav_color = "#FFA500"
        bottom_nav_color = "#EEEEEE"

    elif platform == "linux":
        app_home = str(Path.cwd()) 
        android_home = str(Path.cwd().parents[1])
        primary_ext_storage = str(Path().home())

    elif platform == "windows":
        app_home = str(Path.cwd()) 
        android_home = str(Path.cwd().parents[1])
        primary_ext_storage = str(Path().home())


    kv_dir = app_home + '/kv_files'
    font_dir = app_home + '/assets/fonts'
    img_dir = app_home + '/assets/images'
    # Kivy files
    main_kv_file = kv_dir + "/main.kv"
    login_kv_file = kv_dir + "/login_signout.kv"
    custom_kv_file = kv_dir + "/custom_classes.kv"
    manager_kv_file = kv_dir + "/manager.kv"
    document_page_kv_file = kv_dir + "/document_page.kv"
    profile_file = kv_dir + "/profile.kv"
    
    # Fonts directory
    lato_black = font_dir + "/Lato-Black.ttf"
    lato_bold = font_dir + "/Lato-Bold.ttf"
    lato_regular = font_dir + "/Lato-Regular.ttf"
    lato_light = font_dir + "/Lato-Light.ttf"
    segoe_font = font_dir + "/SEGOEUI.TTF"

    # Image/gifs directory
    loading_gif1 = img_dir + '/gifs/loading1.gif'
    loading_gif2 = img_dir + '/gifs/loading2.gif'
    presplash = img_dir + '/pngs/TMSPresplash2.png'
    # Image/icons directory
    account_icon = img_dir + '/icons/account.png'
    file_icon = img_dir + '/icons/logo1.ico'
    # Image/pngs directory
    toolbar_bg_img1 = img_dir + '/pngs/toolbar_bg.png'
    toolbar_bg_img2 = img_dir + '/pngs/toolbar_bg3.png'

    # color codes
    tab_nav_color = (238/255, 238/255, 238/255, 1)
    tab_bg_color = (249/255, 249/255, 249/255, 1)
    tab_item_color = (1, 1, 1, 1)
    black_color = (0,0,0,1)
    white_color = (1, 1, 1, 1)

    # sudo components
    #local_files = [{'text': f'Project description{i}', 'secondary_text':'Today'} for i in range(33)]
    cloud_files = [{'text': f'Project{i}', 'secondary_text': ''} for i in range(10)]

    # Database Directory
    database_dir = android_home + "/databases"
    search_dirs = {app_home, primary_ext_storage}

    @staticmethod
    def list_dirs(dirname, file=True, folder=True):
        if file and folder:
            return [str(x) for x in Path(dirname).glob('*')]
        elif file:
            return [str(x) for x in Path(dirname).glob('*') if x.is_file()]
        else:
            return [str(x) for x in Path(dirname).glob('*') if not x.is_file()]

    def __init__(self) -> None:
        if platform == "android":
            self.statusbar(self.top_nav_color, self.bottom_nav_color)
