from evdev import UInput, ecodes as e
import pyautogui

def alt_tab():
    pyautogui.hotkey('alt', 'tab')
