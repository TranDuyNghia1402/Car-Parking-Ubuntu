import os
import cv2 as cv
from ultralytics import YOLO


# load model
model_path = '/home/tran-duy-nghia/Desktop/CarParking/CODE/SOURCE/DETECTMODEL/ANPR.pt'
model = YOLO(model_path)
# threshold
threshold = 0.5
# image name of the frame detected license plate
img_name = 'license_plate.jpg'
# path to folder hold the img license plate detected
img_folder = '/home/tran-duy-nghia/Desktop/KLTN/CarParking/IMAGES/STORAGE_IMG/'


class Gate:
    def __init__(self, camera_frame=None, image_input=None) -> None:
        self.frame = camera_frame
        self.image = image_input

    def plate_regconition(self):
        # results = model(self.frame, device='cpu')[0]
        results = model(self.image, device='cpu')[0]
        for result in results.boxes.data.tolist():
            score = result[4]
            if score > threshold:
                path = os.path.join(img_folder, img_name)
                cv.imwrite(path, self.image)
                return True, path
        return False

    def send_command(self, ser, command):
        ser.write(command)
