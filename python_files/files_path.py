
from types import FunctionType


class FileDirectories:
    android_home = "/storage/emulated/0/"
    app_home = "./"
    kv_dir = app_home + 'kv_files/'
    font_dir = app_home + 'assets/fonts/'
    img_dir = app_home + 'assets/images/'
    # Kivy files
    main_kv_file = kv_dir + "main.kv"
    maintabs_kv_file = kv_dir + "main_tabs.kv"
    
    # Fonts directory
    lato_black = font_dir + "Lato-Black.ttf"
    lato_bold = font_dir + "Lato-Bold.ttf"
    lato_regular = font_dir + "Lato-Regular.ttf"
    lato_light = font_dir + "Lato-Light.ttf"

    # Image directory
    loading_gif1 = img_dir + 'gifs/loading1.gif'
    loading_gif2 = img_dir + 'gifs/loading2.gif'
    
