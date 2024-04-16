# import websocket
# import threading
# import json 
# import time 

# def on_error(ws, error):
#     print("Error:", error)

# def on_close(ws):
#     print("### closed ###")

# def on_open(ws):
#     print("### connected ###")

# class Cam_feed():
#     def __init__(self):
#         self.ws_url = "ws://192.168.4.1/CarInput"
#         self.ws = websocket.WebSocketApp(self.ws_url,
#                                     on_error=on_error,
#                                     on_close=on_close)
#         self.ws.on_open = on_open
#         self.thread = threading.Thread(target=self.run_forever_in_thread)
#         self.thread.daemon = True
#         self.thread.start()

#     def run_forever_in_thread(self):
#         print("Camera WebSocket thread started.")
#         self.ws.run_forever()
#         print("Camera WebSocket thread ended.")

#     def send_cmd(self, command):
#         # print(self.ws,self.ws.sock,self.ws.sock.connected)
#         if self.ws and self.ws.sock and self.ws.sock.connected:
#             # Send movement command over WebSocket
#             try:
#                 # self.ws.send(json.dumps({command}))
#                 self.ws.send(command)
#                 print("Done")
#             except:
#                 print("Something wrong")
#         else:
#             print("Camera WebSocket connection is not esta-blished or closed.")


# # Create an instance of Cam_feed
# cam = Cam_feed()

# # Continuously send movement commands
# while True:
#     cam.send_cmd("MoveCar,1")
#     time.sleep(1)

#------------------------------------------------------------------------------------------------------------------------
# import websocket
# import time

# # WebSocket server address
# websocket_server = "ws://192.168.4.1/CarInput"  # Replace with your ESP32-CAM's IP address

# # Function to send movement commands
# def send_command(command):
#     ws.send(command)

# # WebSocket event handlers
# def on_open(ws):
#     print("WebSocket connection opened")
#     # Example: send "UP" command when the WebSocket connection is opened
#     send_command("MoveCar,1")

# def on_message(ws, message):
#     print("Received message:", message)

# def on_error(ws, error):
#     print("WebSocket error:", error)

# def on_close(ws):
#     print("WebSocket connection closed")

# # Create WebSocket connection
# ws = websocket.WebSocketApp(websocket_server,
#                             on_open=on_open,
#                             on_message=on_message,
#                             on_error=on_error,
#                             on_close=on_close)

# # Run WebSocket client
# ws.run_forever()
#------------------------------------------------------------------------------------------------------------------------


import websocket
import threading
import time
from kivy.app import App
from kivy.uix.button import Button

# WebSocket server address
websocket_server = "ws://192.168.4.1/CarInput"  # Replace with your ESP32-CAM's IP address

# Flag to indicate if movement command should be sent
send_movement_flag = False

# Function to send movement commands
def send_command(command):
    global ws
    if ws:
        ws.send(command)

# Function to continuously wait for commands
def wait_for_commands():
    global send_movement_flag
    while True:
        if send_movement_flag:
            send_command("MoveCar,1")
            send_movement_flag = False
        time.sleep(0.1)  # Adjust sleep time as needed

# WebSocket event handlers
def on_open(ws):
    print("WebSocket connection opened")

def on_message(ws, message):
    print("Received message:", message)

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws):
    print("WebSocket connection closed")

# Create WebSocket connection
ws = None

def connect_websocket():
    global ws
    ws = websocket.WebSocketApp(websocket_server,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

# Start waiting for commands in a separate thread
thread = threading.Thread(target=wait_for_commands)
thread.daemon = True
thread.start()

class MyKivyApp(App):
    def build(self):
        button = Button(text='Press to move car')
        button.bind(on_press=self.set_send_movement_flag)
        return button

    def set_send_movement_flag(self, instance):
        global send_movement_flag
        send_movement_flag = True

if __name__ == '__main__':
    # Start WebSocket connection in a separate thread
    websocket_thread = threading.Thread(target=connect_websocket)
    websocket_thread.daemon = True
    websocket_thread.start()
    
    MyKivyApp().run()



