import asyncio
import threading
from dataclasses import dataclass
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from urllib.request import urlopen

import evdev
from evdev import ecodes

from sleuthconf import window
from sleuthconf.obs import OBS
from sleuthconf.trivia import Trivia
from sleuthconf.window import Window


def find_device(name):
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if device.name == name:
            print(f"Found device: {device.path}")
            break
    else:
        print("Can't find clicker, skipping")
        exit(0)
    return device


class Clicker:
    def __init__(self, obs: OBS, window: Window, trivia: Trivia, data: dict):
        self.obs = obs
        self.trivia = trivia
        self.window = window
        self.data = data
        self.device = None

    async def _process_event(self, code):

        if code == ecodes.KEY_PLAYPAUSE:
            self.window.alt_tab()
        elif code == ecodes.KEY_VOLUMEUP:
            self.window.esc()
        elif code == ecodes.KEY_VOLUMEDOWN:
            ext_ip = urlopen('https://api.ipify.org').read()
            self.obs.set_item_property("[text] Question", "text", f"IP: {ext_ip} ")
            self.obs.set_scene("Trivia - Q")
        else:
            print(f"Unknown key: {code}")

        # section = sections[current_section_idx]
        # new_section(obs, "", "")
        # obs.call(requests.SetCurrentScene("Interview - me (title)"))
        # new_section(obs, section["title"], section["byline"])

    async def run(self):
        self.device = find_device("2.4G Composite Devic Wireless Devic Consumer Control")
        with self.device.grab_context():
            print("grabbed context")
            async for event in self.device.async_read_loop():
                if event.type == ecodes.EV_KEY and event.value == 1:
                    try:
                        await self._process_event(event.code)
                    except Exception as e:
                        print(f"Exception processing event: {e}")

    def start(self):
        def go():
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.run())

        t = threading.Thread(target=go, daemon=True)
        t.start()

    def stop(self):
        if self.device:
            self.device.close()


