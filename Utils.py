import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def validate_keys(key: str):
    key = key.capitalize()

    if len(key) == 1: return key
    if key == "Ctrl": return key
    if key == "Ctrl_r": return key
    if key == "Alt": return key
    if key == "Alt_r": return key
    if key == "Alt_gr": return key
    if key == "Shift": return key
    if key == "Shift_r": return key
    if key == "Backspac": return key
    if key == "Nter": return key
    if key == "Sc": return key
    if key == "Tab": return key
    if key == "Caps_lock": return key
    if key == "Cmd": return key
    if key == "Menu": return key
    if key == "Spac": return key

    return ""