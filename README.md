# TMS-Mobile-Reader
An Intelligent document reader targeting the android platform

## To create a new kivy file
* create the kv file in the kv_files directory
* add the file path to the python_files/files_path.FileDirectories
* Build the file directory in the main app of the main.py file.

## To create a widget in another file
* Create the widget in the kv file and/or in the python file (create file if neccessary but make sure it is imported in the import_classes of the mainapp class)
* link the widget to the correct parent in the link_widget class of the main app
