# import torch
# import cv2
# from yolov5.models.experimental import attempt_load
# from yolov5.utils.general import non_max_suppression

# # Load YOLOv8 model
# model = attempt_load("yolov8n.pt")

# # Prepare image
# img = cv2.imread("images.jpeg")
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to RGB format
# img_tensor = torch.from_numpy(img).float()  # Convert image to tensor
# img_tensor /= 255.0  # Normalize pixel values to range [0, 1]
# img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension

# # Perform inference
# model.eval()
# with torch.no_grad():
#     pred = model(img_tensor)[0]

# # Apply non-maximum suppression
# pred = non_max_suppression(pred, conf_thres=0.4, iou_thres=0.5)

# # Draw bounding boxes
# for det in pred[0]:
#     # det format: [x1, y1, x2, y2, conf, cls]
#     bbox = det[:4].cpu().numpy()
#     label = det[5].cpu().numpy()
#     bbox[2:] -= bbox[:2]  # Convert from (x1, y1, x2, y2) to (x1, y1, w, h)
#     bbox = [int(coord) for coord in bbox]  # Convert to integers
#     cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)  # Draw rectangle
#     cv2.putText(img, f"Class: {label}", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Put text

# # Display or save image with bounding boxes
# img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert image back to BGR format
# cv2.imshow("Result", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import threading
import websocket
import time

# WebSocket server address
websocket_server = "ws://192.168.4.1/CarInput"  # Replace with your ESP32-CAM's IP address

# Flag to indicate if movement command should be sent
send_movement_flag = False

# Commands dictionary
commands = {
    "Stop":"MoveCar,0",
    "Forward": "MoveCar,1",
    "Backward": "MoveCar,2",
    "Left": "MoveCar,3",
    "Right": "MoveCar,4"
}

# Function to send movement commands
def send_command(command):
    global ws
    if ws:
        ws.send(command)

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

def set_send_movement_flag(command):
    global send_movement_flag
    send_movement_flag = True
    send_command(command)

def Stop_cmd(ins):
    global send_movement_flag
    send_command(commands["Stop"])
    send_movement_flag = False

class ControlPanel(GridLayout):
    def __init__(self, **kwargs):
        super(ControlPanel, self).__init__(**kwargs)
        self.cols = 2

        # Movement buttons
        f = Button(text="Forward", on_press=lambda instance: set_send_movement_flag(commands["Forward"]))
        f.bind(on_release = Stop_cmd)
        self.add_widget(f)
        self.add_widget(Button(text="Backward", on_press=lambda instance: set_send_movement_flag(commands["Backward"])))
        self.add_widget(Button(text="Left", on_press=lambda instance: set_send_movement_flag(commands["Left"])))
        self.add_widget(Button(text="Right", on_press=lambda instance: set_send_movement_flag(commands["Right"])))

class ControlApp(App):
    def build(self):
        return ControlPanel()

# Start WebSocket connection in a separate thread
websocket_thread = threading.Thread(target=connect_websocket)
websocket_thread.daemon = True
websocket_thread.start()

if __name__ == "__main__":
    ControlApp().run()
