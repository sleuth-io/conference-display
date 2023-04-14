import asyncio
import threading
from dataclasses import dataclass
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import evdev
from evdev import ecodes

from sleuthconf import window
from sleuthconf.obs import OBS
from sleuthconf.trivia import Trivia


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
    def __init__(self, obs: OBS, trivia: Trivia, data: dict):
        self.obs = obs
        self.trivia = trivia
        self.data = data
        self.device = None
        self.driver = None

    async def _process_event(self, code):

        # if code == ecodes.KEY_RIGHT:
        #     # current_section_idx += 1
        #     # if len(sections) == current_section_idx:
        #     #     current_section_idx = 0
        #     await broadcast_to_clients("next")
        # elif code == ecodes.KEY_LEFT:
        #     await broadcast_to_clients("prev")
        #
        # elif code == ecodes.KEY_POWER:
        #     obs.call(requests.SetCurrentScene("Slides - Green screen"))
        # elif code == ecodes.KEY_PLAYPAUSE:
        #     obs.call(requests.SetCurrentScene("Slides - Green screen (zoom)"))
        # elif code == ecodes.KEY_COMPOSE:
        #     obs.call(requests.SetCurrentScene("Slides - Firefox"))
        # elif code == ecodes.KEY_BACK:
        #     obs.call(requests.SetCurrentScene("Coding - Webcam"))
        # elif code == ecodes.KEY_UP:
        #     obs.call(requests.SetSceneItemRender("Window chat", True))
        # elif code == ecodes.KEY_DOWN:
        #     obs.call(requests.SetSceneItemRender("Window chat", False))
        if code == ecodes.KEY_PLAYPAUSE:
            window.alt_tab()
            pass # obs.set_scene("requests.SetCurrentScene("Slides - Video"))
        if code == ecodes.KEY_VOLUMEUP:
            from selenium import webdriver

            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--no-sandbox")
            chromeOptions.add_argument("--disable-setuid-sandbox")
            chromeOptions.add_argument("--disable-dev-shm-using")
            chromeOptions.add_argument("--disable-extensions")
            chromeOptions.add_argument("start-maximized")
            chromeOptions.add_argument("disable-infobars")
            chromeOptions.add_argument("--remote-debugging-port=9222")
            driver = webdriver.Chrome(chrome_options=chromeOptions)
            driver.get('https://app.sleuth.io/sleuth/sleuth')
            driver.fullscreen_window()
            self.driver = driver
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


