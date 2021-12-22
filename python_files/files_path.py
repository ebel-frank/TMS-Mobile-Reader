

class FileDirectories:
    android_home = "/storage/emulated/0/"
    app_home = "./"
    kv_dir = app_home + 'kv_files/'
    font_dir = app_home + 'assets/fonts/'
    img_dir = app_home + 'assets/images/'
    # Kivy files
    main_kv_file = kv_dir + "main.kv"
    login_kv_file = kv_dir + "login_signout.kv"
    custom_kv_file = kv_dir + "custom_classes.kv"
    manager_kv_file = kv_dir + "manager.kv"
    
    # Fonts directory
    lato_black = font_dir + "Lato-Black.ttf"
    lato_bold = font_dir + "Lato-Bold.ttf"
    lato_regular = font_dir + "Lato-Regular.ttf"
    lato_light = font_dir + "Lato-Light.ttf"
    segoe_font = font_dir + "SEGOEUI.TTF"

    # Image/gifs directory
    loading_gif1 = img_dir + 'gifs/loading1.gif'
    loading_gif2 = img_dir + 'gifs/loading2.gif'
    # Image/icons directory
    account_icon = img_dir + 'icons/account.png'
    file_icon = img_dir + 'icons/logo1.ico'
    # Image/pngs directory
    toolbar_bg_img1 = img_dir + 'pngs/toolbar_bg.png'
    toolbar_bg_img2 = img_dir + 'pngs/toolbar_bg3.png'

    # color codes
    tab_nav_color = (238/255, 238/255, 238/255, 1)
    tab_bg_color = (249/255, 249/255, 249/255, 1)
    tab_item_color = (1, 1, 1, 1)
    black_color = (0,0,0,1)
    white_color = (1, 1, 1, 1)

    # sudo components
    local_files = [[f'Project description{i}', 'Today'] for i in range(33)]
    cloud_files = [[f'Project description{i}', ' '] for i in range(21)]
