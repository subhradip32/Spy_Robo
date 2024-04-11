from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import matplotlib
matplotlib.use('TkAgg')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from kivy.clock import Clock
import cv2 as cv
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
import requests
import Camera 
        


def redeffine_data(data):
    res = list() 
    for i in range(len(data)):
        x = [0,data[i]]
        res.append(x)
    return res 

class PolarPlotApp(App):
    def radar(self, dt):
        # Clear the previous plot
        plt.clf()
        # Creating the polar plot
        fig = plt.figure(dpi=100)
        ax = fig.add_subplot(projection='polar')
        ax.set_thetamin(0)
        ax.set_thetamax(180)
        
        # Generating the X and Y axis data points
        # self.r = np.random.randint(10,100,15)
        # theta = np.deg2rad(np.random.randint(45,135,15))
        
        self.r = [[0,10],[0,10],[0,10],[0,5],[0,6],[0,7],[0,10],[0,10],[0,10],[0,10]]
        # theta = np.arange(0,180,10)
        theta = [[0,0],[0,18],[0,36],[0,54],[0,72],[0,90],[0,108],[0,126],[0,44],[0,162]]

        for i in range(len(self.r)):
            ax.plot(theta[i],self.r[i],color = "r")
        
        # Plotting each point separately dot plot 
        # for i in range(len(self.r)):
            # ax.plot(theta[i], self.r[i], marker='o', color="r")
        # Setting the axis limit
        # ax.set_ylim(0, max(self.r) + 2)

        #generating the

        ax.set_ylim(0,10)
        
        ax.set_facecolor("lightgreen")
        # Create a canvas for the plot
        canvas = FigureCanvas(fig)
        self.layout.clear_widgets()
        self.layout.add_widget(canvas)

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        # Schedule the update function to run every 1 second
        Clock.schedule_interval(self.radar, 1)

        return self.layout




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

        if frame is not None:
            # Convert frame to texture and assign to image widget
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture
        
        print(frame)



red = [1, 0, 0, 1]  
green = [0, 1, 0, 1]  
blue = [0, 0, 1, 1]  
purple = [1, 0, 1, 1]
white = [1,1,1,1]

class Grid():
    def all_layout(self):
        main_layout = GridLayout(cols=2)

        obstacle = PolarPlotApp()
        main_layout.add_widget(obstacle.build())
        
        # main_layout.add_widget(Label(text="Radar Display"))
        # read = CamFeed()
        # main_layout.add_widget(Label(text="Camera Display"))
        main_layout.add_widget(OpenCVCamera())
        
        # main_layout.add_widget(OpenCVCamera())

        # Movement buttons 
        move_layout = GridLayout(cols=1)
        move_layout.add_widget(Button(text="^"))

        # samller section
        sub_layout = GridLayout(cols=2)
        sub_layout.add_widget(Button(text="<"))
        sub_layout.add_widget(Button(text=">"))

        move_layout.add_widget(sub_layout)
        move_layout.add_widget(Button(text="V"))
        move_layout.add_widget(Label(text = "Data of output:--------------> ",color = purple))


        cam_move = GridLayout(cols=1)
        cam_move.add_widget(Button(text = "Cam^",background_color = red))
        #samll cam 
        sub_cam = GridLayout(cols= 2)
        sub_cam.add_widget(Button(text = "<",background_color = red))
        sub_cam.add_widget(Button(text = ">",background_color = red))
        cam_move.add_widget(sub_cam)
        cam_move.add_widget(Button(text = "Camv",background_color = red))

        cam_move.add_widget(Button(text="Download Data",color = white,background_color = green))


        main_layout.add_widget(move_layout)
        main_layout.add_widget(cam_move)
        return main_layout

class TestApp(App):
    def build(self):
        grid_instance = Grid()
        return grid_instance.all_layout()
    
TestApp().run()


# creating the ml configuration on it 