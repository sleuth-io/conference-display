import argparse
import random
import textwrap
import time

from sleuthconf.obs import OBS
from sleuthconf.trivia import Trivia


def on_connect(obs):
    obs.call("OpenVideoMixProjector", {
        "videoMixType": "OBS_WEBSOCKET_VIDEO_MIX_TYPE_PREVIEW",
        "monitorIndex": 1
    })
    obs.set_scene("Coding - Pycharm")


def main():
    parser = argparse.ArgumentParser(description="The trivial file")
    parser.add_argument("trivia", help="The trivia YAML file")
    opts = parser.parse_args()

    trivia = Trivia(opts.trivia)
    obs = OBS("sleuth", on_connect=on_connect)

    resp = obs.call("GetSceneItemId", {
        "sceneName": "Coding - Pycharm",
        "sourceName": "Text_Question",
    })
    question_item_id = resp.scene_item_id

    try:
        while True:
            question = random.choice(trivia.questions)
            q_wrapped = textwrap.fill(question.name, width=30)
            transform = obs.call("GetSceneItemTransform", {
                "sceneName": "Coding - Pycharm",
                "sceneItemId": question_item_id
            }).scene_item_transform
            transform |= {
                "positionX": 0,
                "positionY": 600,
                "boundsWidth": 1920,
                "boundsHeight": 300
            }
            obs.call("SetSceneItemTransform", {
                "sceneName": "Coding - Pycharm",
                "sceneItemId": question_item_id,
                "sceneItemTransform": transform
            })
            a_wrapped = textwrap.fill(question.answer, width=30)
            obs.set_item_property("Text_Question", "text", q_wrapped)
            obs.set_item_property("Text_Answer", "text", a_wrapped)
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    print("done!")


if __name__ == "__main__":
    main()

