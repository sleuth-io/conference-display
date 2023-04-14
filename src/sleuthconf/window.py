from evdev import UInput, ecodes as e


def alt_tab():
    ui = UInput()
    ui.write(e.EV_KEY, e.KEY_TAB, 1)
    ui.write(e.EV_KEY, e.KEY_LEFTALT, 1)
    ui.write(e.EV_KEY, e.KEY_TAB, 0)
    ui.write(e.EV_KEY, e.KEY_LEFTALT, 0)
    ui.syn()
