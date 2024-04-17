import cv2
import numpy as np
from io import BytesIO
import threading
import websocket

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### connected ###")

class Cam_feed():
    def __init__(self):
        self.ws_url = "ws://192.168.4.1/Camera"
        self.image = None
        self.ws = websocket.WebSocketApp(self.ws_url,
                                    on_message=self.on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        self.ws.on_open = on_open
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()

    def on_message(self, ws, message):
        # Received image data
        image_stream = BytesIO(message)
        # Decode image bytes to numpy array
        self.image = cv2.imdecode(np.frombuffer(image_stream.read(), dtype=np.uint8), cv2.IMREAD_COLOR)

    def get_frame(self):
        return self.image