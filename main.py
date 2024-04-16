from kivy.app import App
from kivy.uix.button import Button 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import matplotlib
matplotlib.use('TkAgg')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FigureCanvas
from kivy.clock import Clock
import cv2 as cv
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
import threading
import websocket
import Camera 
import Objectdetection

# # Declaring a golbal values 
red = [1, 0, 0, 1]  
green = [0, 1, 0, 1]  
blue = [0, 0, 1, 1]  
purple = [1, 0, 1, 1]
white = [1,1,1,1]
Cam_feed_global = None

class CamMLFilter(BoxLayout):
    def __init__(self):
        super(CamMLFilter, self).__init__()
        self.filter = filter 
        global Cam_feed_global
        self.filter_image = Cam_feed_global 

        self.img = Image() 
        self.add_widget(self.img)
        
        # Updating the cam feed using the Clock
        Clock.schedule_interval(self.update, 1.0 / 120.0)

    def update(self, dt):
        global Cam_feed_global
        self.filter_image = Cam_feed_global

        if Cam_feed_global is not None:
            texture = Texture.create(size=(self.filter_image.shape[1], self.filter_image.shape[0]))
            
            self.apply_ML_filter()

            texture.blit_buffer(self.filter_image.tobytes(), bufferfmt='ubyte')
            self.img.texture = texture
    
    def apply_ML_filter(self):

        grayscale_frame = cv.cvtColor(self.filter_image, cv.COLOR_BGR2GRAY)
        heatmap = cv.applyColorMap(grayscale_frame, cv.COLORMAP_JET)
        heatmap = cv.bitwise_not(heatmap)
        self.filter_image =  cv.cvtColor(heatmap, cv.COLOR_RGB2BGR)
        # self.filter_image = Objectdetection.DetectObject().get_faces(self.filter_image)
        self.filter_image = Objectdetection.DetectObject().create_bounding_box(self.filter_image)

class OpenCVCamera(BoxLayout):
    def __init__(self, **kwargs):
        super(OpenCVCamera, self).__init__(**kwargs)

        self.cam_data = Camera.Cam_feed()
        self.img = Image()
        self.add_widget(self.img)

        # Updating the cam feed using the Clock
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        frame = self.cam_data.get_frame()
        frame = cv.flip(frame,-1)
        
        # passing the data to the FilterFunction
        global Cam_feed_global
        Cam_feed_global = frame 

        if frame is not None:
            # Convert frame to texture and assign to image widget
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

# Adding new ---------------------------------------------------------------------------
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
    "Right": "MoveCar,4",
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


class Grid():
    def all_layout(self):
        main_layout = GridLayout(cols=1)

        Cam_grid = GridLayout(cols = 2)
        Cam_grid.add_widget(OpenCVCamera())
        Cam_grid.add_widget(CamMLFilter())
        
        # main_layout.add_widget(OpenCVCamera())

        main_layout.add_widget(Cam_grid)

        # Movement buttons 
        move_layout = GridLayout(cols=1)
        
        forw_btn = Button(text="^",on_press=lambda instance: set_send_movement_flag(commands["Forward"]))
        forw_btn.bind(on_release = Stop_cmd)
        move_layout.add_widget(forw_btn)

        # samller section
        sub_layout = GridLayout(cols=2)
        # sub_layout.add_widget(Button(text="<",on_press = MoveLeft))
        left_btn = Button(text="<",on_press=lambda instance: set_send_movement_flag(commands["Left"]))
        left_btn.bind(on_release = Stop_cmd)
        sub_layout.add_widget(left_btn)
        
        # sub_layout.add_widget(Button(text=">",on_press = MoveRight))
        right_btn = Button(text=">",on_press=lambda instance: set_send_movement_flag(commands["Right"]))
        right_btn.bind(on_release = Stop_cmd)
        sub_layout.add_widget(right_btn)

        move_layout.add_widget(sub_layout)

        # move_layout.add_widget(Button(text="V",on_press = MoveBackward))
        back_btn = Button(text="v",on_press=lambda instance: set_send_movement_flag(commands["Backward"]))
        back_btn.bind(on_release = Stop_cmd)
        move_layout.add_widget(back_btn)

        main_layout.add_widget(move_layout)
        # main_layout.add_widget(cam_move)
        return main_layout

class TestApp(App):
    def build(self):
        grid_instance = Grid()
        return grid_instance.all_layout()
    

# Start WebSocket connection in a separate thread
websocket_thread = threading.Thread(target=connect_websocket)
websocket_thread.daemon = True
websocket_thread.start()
TestApp().run()