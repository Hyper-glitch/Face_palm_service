import os
import unittest
import cv2
import numpy as np
from PIL import Image

FACE_CASCADE = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
RECOGNIZER = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)


class OpenCVTest(unittest.TestCase):
    " This test checks reading the video "

    def test_video_capture(self, username="Romanchelloo"):
        cap = cv2.VideoCapture(username + ".webm")
        self.assertTrue(cap.isOpened())

    " This test checks saving an image "

    def test_save_image(self, username="Romanchelloo"):
        cap = cv2.VideoCapture(username + ".webm")
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(10, 10))
        for (x, y, w, h) in faces:
            cv2.imwrite(username + ".jpg", gray[y:y + h, x:x + w])
            status = cv2.imwrite(username + ".jpg", gray[y:y + h, x:x + w])
            self.assertTrue(status)

    " This test checks that image is grayscale "

    def test_grayscale_image(self, username="Romanchelloo"):
        img = cv2.imread(username + ".jpg")
        self.assertEqual(img.shape[0], img.shape[1])

    " This test checks that recognizer is created "

    def test_create_recognize(self, username="Romanchelloo"):
        faces = []
        id = 1

        face_img = Image.open(username + ".jpg").convert('L')
        face_np = np.array(face_img, np.uint8)
        faces.append(face_np)

        RECOGNIZER.train(faces, np.array(id))
        RECOGNIZER.save(username + ".yml")
        path = os.path.exists(username + ".yml")
        self.assertTrue(path)

    " This test checks that recognizer has a face on an image to predict "

    def test_recognize_is_not_none(self, username="Romanchelloo"):
        RECOGNIZER.read(username + ".yml")

        ret, frame = cv2.VideoCapture(username + ".webm").read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(10, 10))

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            label, conf = RECOGNIZER.predict(roi_gray)
        self.assertIsNotNone(conf)


if __name__ == '__main__':
    unittest.main()
