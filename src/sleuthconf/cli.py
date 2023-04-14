import argparse
import asyncio
import random
import textwrap
import time

import yaml

from sleuthconf.clicker import Clicker
from sleuthconf.demo import Demo
from sleuthconf.obs import OBS
from sleuthconf.trivia import Trivia
from sleuthconf.window import Window


def main():
    parser = argparse.ArgumentParser(description="The trivial file")
    parser.add_argument("trivia", help="The trivia YAML file")
    opts = parser.parse_args()

    with open(opts.trivia, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

    window = Window()
    trivia = Trivia(data)
    demo = Demo()

    def on_connect(obs):
        demo.start()
        obs.call("OpenVideoMixProjector", {
            "videoMixType": "OBS_WEBSOCKET_VIDEO_MIX_TYPE_PREVIEW",
            "monitorIndex": 1
        })

    obs = OBS("sleuth", on_connect=on_connect)
    obs.start_fullscreen_preview()
    clicker = Clicker(obs, window, trivia, data)
    clicker.start()

    try:
        while True:
            obs.set_scene("Homepage")
            time.sleep(5)
            for batch in range(3):
                question = random.choice(trivia.questions)
                set_trivia_text(obs, "Trivia - Q", "[text] Question", question.name)
                set_trivia_text(obs, "Trivia - A", "[text] Answer", question.answer)
                obs.set_item_property("[text] Timer", "text", " ")
                obs.set_scene("Trivia - Q")
                countdown_trivia_timer(obs, 5)
                obs.set_scene("Trivia - A")
                countdown_trivia_timer(obs, 5)
    except KeyboardInterrupt:
        pass
    clicker.stop()
    print("done!")


def set_trivia_timer_enabled(obs, name, enabled):
    resp = obs.call("GetSceneItemId", {
        "sceneName": "[Scene] Trivia",
        "sourceName": f"[v] Timer - {name}",
    })
    item_id = resp.scene_item_id
    obs.call("SetSceneItemEnabled", {
        "sceneName": "[Scene] Trivia",
        "sceneItemId": item_id,
        "sceneItemEnabled": enabled,
    })


def countdown_trivia_timer(obs, seconds):
    time.sleep(2)
    for cur in range(seconds, -1, -1):
        obs.set_item_property("[text] Timer", "text", str(cur))
        time.sleep(1)

    obs.set_item_property("[text] Timer", "text", " ")


def set_trivia_text(obs, scene_name, item_name, text):
    resp = obs.call("GetSceneItemId", {
        "sceneName": scene_name,
        "sourceName": item_name,
    })
    item_id = resp.scene_item_id
    transform = obs.call("GetSceneItemTransform", {
        "sceneName": scene_name,
        "sceneItemId": item_id
    }).scene_item_transform
    transform |= {
        "positionX": 50,
        "positionY": 150,
        "boundsWidth": 1920,
        "boundsHeight": 300
    }
    obs.call("SetSceneItemTransform", {
        "sceneName": scene_name,
        "sceneItemId": item_id,
        "sceneItemTransform": transform
    })
    a_wrapped = textwrap.fill(text, width=30)
    obs.set_item_property(item_name, "text", a_wrapped)


if __name__ == "__main__":
    main()

