import argparse
import asyncio
import random
import textwrap
import time

import yaml

from sleuthconf.clicker import Clicker
from sleuthconf.obs import OBS
from sleuthconf.trivia import Trivia


def on_connect(obs):
    obs.call("OpenVideoMixProjector", {
        "videoMixType": "OBS_WEBSOCKET_VIDEO_MIX_TYPE_PREVIEW",
        "monitorIndex": 1
    })


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

    trivia = Trivia(data)
    obs = OBS("sleuth", on_connect=on_connect)
    clicker = Clicker(obs, trivia, data)
    clicker.start()

    try:
        while True:
            obs.set_scene("Homepage")
            question = random.choice(trivia.questions)
            set_trivia_text(obs, "Trivia - Q", "[text] Question", question.name)
            set_trivia_text(obs, "Trivia - A", "[text] Answer", question.answer)
            set_trivia_timer_enabled(obs, "10s", False)
            set_trivia_timer_enabled(obs, "30s", False)
            time.sleep(5)
            obs.set_scene("Trivia - Q")
            time.sleep(2)
            set_trivia_timer_enabled(obs, "30s", True)
            time.sleep(5)
            set_trivia_timer_enabled(obs, "30s", False)
            obs.set_scene("Trivia - A")
            set_trivia_timer_enabled(obs, "10s", True)
            time.sleep(10)
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

