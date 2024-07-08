import os
import requests
import cv2
import numpy as np

def downloadFile(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded file to {local_path}")
    else:
        print(
            f"Failed to download file from {url}. Status code: {response.status_code}"
        )


def checkAndDownloaFile(local_path, url):
    if os.path.exists(local_path):
        print(f"File already exists: {local_path}")
    else:
        print(f"File does not exist. Downloading from {url}")
        downloadFile(url, local_path)


def calculateEuclide(point1: np.ndarray, point2: np.ndarray):
    return np.linalg.norm(point1 - point2)

def convertImage(image):
        height, width, _ = image.shape
        if width/height != 3/4:
            new_width = int((3 / 4) * height)
            image_converted = cv2.resize(image, (new_width, height))
            return image_converted
        else:
            return image
