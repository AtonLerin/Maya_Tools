import os

file_path = os.path.dirname(__file__)
ui_path = os.path.split(file_path)[0]

ICON_PATH = os.path.normpath(os.path.join(ui_path, 'ui_tools', 'icons'))
MARKINGMENU_ICONS = os.path.normpath(os.path.join(ui_path, 'ui_tools', 'icons', 'markingmenu_icons'))