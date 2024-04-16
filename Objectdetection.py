import cv2 as cv
from ultralytics import YOLO

class DetectObject():
    def __init__(self) -> None:
        # self.model = YOLO("yolov8m") #takes around more than 200ms 
        self.model = YOLO("yolov8n") #takes around more than 50ms 
        # self.model.cuda(0)
        self.model.cpu()

        self.face_cascade = cv.CascadeClassifier("haarcascade-frontalface-default.xml")
        self.fullbody_detection = cv.CascadeClassifier("haarcascade_fullbody.xml")

    def create_bounding_box(self, frame):
        results = self.model(frame)
        for result in results:
            for each in result.boxes.xywh:
                x_center, y_center, w, h = each  # Get center x, y, width, height
                x = x_center - w / 2  # Calculate top-left x
                y = y_center - h / 2  # Calculate top-left y
                cv.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), (255, 0, 0), 3)
        return frame  # Return the original color image with bounding boxes drawn

    def get_faces(self,frame):
        gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

        #detecting faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 5)
        
        full_body = self.fullbody_detection.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in full_body:
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)

        return frame