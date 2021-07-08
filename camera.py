import logging
import shutil
import time
import cv2
import os
from PIL import Image
import numpy as np

FACE_CASCADE = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
RECOGNIZER = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
LOGGER = logging.getLogger(__name__)


class VideoCamera:
    def __init__(self, username):
        self.username = username

    # This function allows you to transform video to JPG
    def transform_to_jpeg(self):
        path = f"datasets/{self.username}/{self.username}"
        cap = cv2.VideoCapture(path + ".webm")
        idx = 0
        while (cap.isOpened()):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(10, 10))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imwrite(path + "." + str(idx) + ".jpg", gray[y:y + h, x:x + w])
                time.sleep(0.1)
                idx += 1
            if idx == 20:
                break

        LOGGER.info(f'Photos were created!')
        cap.release()

    # Delete the video file to reduce the storage
    def delete_video(self):
        path = f"datasets/{self.username}/{self.username}" + ".webm"
        if os.path.exists(path):
            os.remove(path)
            LOGGER.info(f'The video removed from dataset!')

    # This function will create a trainer file to compare faces
    def create_recognizer(self):
        path = f"datasets/{self.username}"
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        pseudo_labels = []
        id = 1

        for image_path in image_paths:
            if ".yml" in image_path:
                pass
            else:
                face_img = Image.open(image_path).convert('L')
                face_np = np.array(face_img, np.uint8)
                pseudo_labels.append(id)
                faces.append(face_np)
        return faces, np.array(pseudo_labels)

    def recognize(self):
        RECOGNIZER.read(f"datasets/{self.username}/{self.username}" + ".yml")
        ret, frame = cv2.VideoCapture(f"tempdata/{self.username}/{self.username}" + ".webm").read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(10, 10))
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            label, conf = RECOGNIZER.predict(roi_gray)
            return conf

    # Delete the video file to reduce the storage
    def delete_video_from_tempdata(self):
        path = f"tempdata/{self.username}"
        if os.path.exists(path):
            shutil.rmtree(path)
            LOGGER.info(f'The video removed from tempdata')
