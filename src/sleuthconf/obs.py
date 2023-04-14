import base64
import hashlib
import json
from functools import partial
from json import JSONDecodeError
from random import randint
from time import sleep
from typing import Any

import websocket
from obsws_python.error import OBSSDKError
from obsws_python.util import as_dataclass
from websocket import WebSocketConnectionClosedException, WebSocketException


# Copied from obsws_python 1.1.1, fixed to support reconnection
class ReconnectingObsClient:
    DELAY = 0.001

    def __init__(self, host: str, port: int, password: str, on_connect = None):
        self.ws = websocket.WebSocket()
        self.host = host
        self.port = port
        self.password = password
        self.on_connect = on_connect
        self.subs = 0
        self._connected = False

    def connect(self):
        if not self._connected:
            while True:
                try:
                    self.ws.connect(f"ws://{self.host}:{self.port}")
                    self._authenticate(json.loads(self.ws.recv()))
                    self._connected = True
                    if self.on_connect:
                        self.on_connect()
                    break
                except ConnectionError as ex:
                    print(f"Unable to connect: {ex}. Try again...")
                    sleep(3)

    def _authenticate(self, server_hello):
        secret = base64.b64encode(
            hashlib.sha256(
                (
                    self.password + server_hello["d"]["authentication"]["salt"]
                ).encode()
            ).digest()
        )

        auth = base64.b64encode(
            hashlib.sha256(
                (
                    secret.decode()
                    + server_hello["d"]["authentication"]["challenge"]
                ).encode()
            ).digest()
        ).decode()

        payload = {
            "op": 1,
            "d": {
                "rpcVersion": 1,
                "authentication": auth,
                "eventSubscriptions": self.subs,
            },
        }

        self.ws.send(json.dumps(payload))
        return self.ws.recv()

    def req(self, req_type, req_data=None):
        self.connect()
        if req_data:
            payload = {
                "op": 6,
                "d": {
                    "requestType": req_type,
                    "requestId": randint(1, 1000),
                    "requestData": req_data,
                },
            }
        else:
            payload = {
                "op": 6,
                "d": {"requestType": req_type, "requestId": randint(1, 1000)},
            }
        try:
            self.ws.send(json.dumps(payload))
            response = json.loads(self.ws.recv())
        except (JSONDecodeError, ConnectionError, WebSocketException) as ex:
            print(f"Disconnected: {ex}")
            self._connected = False
            return self.req(req_type, req_data=req_data)

        return response["d"]


class OBS:
    def __init__(self, password: str,
                 host: str = "localhost",
                 port: int = 4444,
                 on_connect = None):
        if not password:
            raise ValueError("Missing password for obs")
        self._started = False
        self.client = ReconnectingObsClient(host=host, port=port, password=password, on_connect=partial(on_connect, self))

    def set_scene_item_enabled(self, scene: str, name: str, enabled: bool = True):
        resp = self.call("GetSceneItemId", {
            "sceneName": scene,
            "sourceName": name,
        })
        self.call("SetSceneItemEnabled", {
            "sceneName": scene,
            "sceneItemId": resp.scene_item_id,
            "sceneItemEnabled": enabled,
        })

    def start_fullscreen_preview(self):
        self.call("OpenVideoMixProjector", {
            "videoMixType": "OBS_WEBSOCKET_VIDEO_MIX_TYPE_PREVIEW",
            "monitorIndex": 0
        })

    def set_scene(self, name: str):
        self.call("SetCurrentProgramScene", {"sceneName": name})

    def set_item_property(self, name: str, property: str, value: Any):
        self.call("SetInputSettings", {"inputName": name,
                                           "inputSettings": {property: value},
                                           "overlay": True})

    def call(self, param, data=None) -> Any:
        response = self.client.req(param, data)

        if not response["requestStatus"]["result"]:
            error = (
                f"Request {response['requestType']} returned code {response['requestStatus']['code']}",
            )
            if "comment" in response["requestStatus"]:
                error += (f"With message: {response['requestStatus']['comment']}",)
            raise OBSSDKError("\n".join(error))
        if "responseData" in response:
            return as_dataclass(response["requestType"], response["responseData"])
