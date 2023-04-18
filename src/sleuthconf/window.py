from evdev import UInput, ecodes as e


class Window:
    def __init__(self):
        self.input = UInput({e.EV_KEY : [e.KEY_LEFTALT, e.KEY_TAB, e.KEY_VOLUMEUP, e.KEY_VOLUMEDOWN]})

    def alt_tab(self):
        print("tabbing")
        self.input.write(e.EV_KEY, e.KEY_LEFTALT, 1)
        self.input.write(e.EV_KEY, e.KEY_TAB, 1)
        self.input.write(e.EV_KEY, e.KEY_TAB, 0)
        self.input.write(e.EV_KEY, e.KEY_LEFTALT, 0)
        self.input.syn()

    def esc(self):
        self.input.write(e.EV_KEY, e.KEY_ESC, 1)
        self.input.write(e.EV_KEY, e.KEY_ESC, 0)
        self.input.syn()

