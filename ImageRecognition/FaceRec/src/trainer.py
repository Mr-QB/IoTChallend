import re
from arcface import ArcFace
from .utility import checkAndDownloaFile
import numpy as np
import os
import cv2
import pandas as pd
from src.faceDetect import FaceDetector
from src.setting import *


class Trainer:
    def __init__(self):
        checkAndDownloaFile(ARCFACE_MODEL_PATH, ARCFACE_MODEL_URL)
        self.face_rec = ArcFace.ArcFace(ARCFACE_MODEL_PATH)
        self.folder_data = FOLDERDATA
        self.face_detector = FaceDetector()

    def train(self):
        self.face_data = []
        valid_extensions = (".jpg", ".jpeg", ".png")

        for filename in os.listdir(self.folder_data):
            if filename.lower().endswith(valid_extensions):
                file_path = os.path.join(self.folder_data, filename)
                image = cv2.imread(file_path)

                if image is None:
                    print(f"Error: Unable to load image at {file_path}")
                    continue

                faces_cropped, x, y = self.face_detector.detect_face(image)
                if faces_cropped is not None:
                    emb1 = self.face_rec.calc_emb(faces_cropped)
                    label = os.path.splitext(filename)[0]
                    label = re.sub(r"\d+", "", label)
                    self.face_data.append([label, emb1])

        # Chuyển self.face_data thành DataFrame
        self.face_data = pd.DataFrame(self.face_data, columns=["label", "embedding"])
        print(self.face_data)

        # # Chuyển đổi embedding thành định dạng numpy array
        # self.face_data["embedding"] = self.face_data["embedding"].apply(
        #     lambda x: np.array(x, dtype=np.float32)
        # )

        # Lưu DataFrame vào file HDF5
        self.face_data.to_hdf("faceData/face_data.h5", key="df", mode="w")
