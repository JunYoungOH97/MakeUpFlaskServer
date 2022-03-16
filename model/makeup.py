from PIL import Image
from model.detection import Detection
import cv2
import numpy as np
import urllib

class MAKEUP():
    def __init__(self, transform, source, target):
        self.transform = transform
        self.A_img = source
        self.B_img = target
        self.detector = Detection()

    def read_img(self, img):
        print(f"Read image : {img}")
        resp = urllib.request.urlopen(img)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def get_item(self):
        # image_A = Image.open(self.A_img).convert("RGB")
        # image_B = Image.open(self.B_img).convert("RGB")
        image_A = self.read_img(self.A_img)
        image_B = self.read_img(self.B_img)

        image_A = Image.fromarray(self.detector.get_image(image_A)[0])
        image_B = Image.fromarray(self.detector.get_image(image_B)[0])

        return self.transform(image_A), self.transform(image_B)

    def __len__(self):
            return 1