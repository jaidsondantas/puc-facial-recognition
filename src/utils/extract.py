from PIL import Image
from mtcnn.mtcnn import MTCNN
from numpy import asarray
import numpy as np

detector = MTCNN()
add = 10


def extract_face(img, size=(320, 320)):
    # img - img.convert("RGB")
    array = asarray(img)
    results = detector.detect_faces(array)
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height

    face = array[(y1 - add):(y2 + add), (x1 - add):(x2 + add)]

    image = Image.fromarray(face)
    image = image.resize(size)
    image.save("./faces/" + str(x1) + ".jpeg", "JPEG")

    return asarray(image)


def extract_faces(img, size=(320, 320)):
    array = asarray(img)
    faces = []
    positons = []
    facesBox = detector.detect_faces(array)
    for faceBox in facesBox:
        x1, y1, width, height = faceBox['box']
        x2, y2 = x1 + width, y1 + height
        # face = array[(y1 - add):(y2 + add), (x1 - add):(x2 + add)]
        face = array[y1:y2, x1:x2]
        image = Image.fromarray(face)
        image = image.resize(size)
        faces.append(asarray(image))
        positons.append([y2, x2, y1, x1])

        # image.save("./faces/" + str(x1) + ".jpeg", "JPEG")

    return faces, positons


def detector_location(img):
    array = asarray(img)
    facesBox = detector.detect_faces(array)
    x1, y1, width, height = facesBox[0]['box']
    x2, y2 = x1 + width, y1 + height
    return [y1, y2, x1, x2]


##Keras

def extract_face_keras(image, box, size=(160, 160)):
    pixels = np.asarray(image)
    x1, y1, width, height = box
    x2, y2 = x1 + width, y1 + height
    face = pixels[y1:y2, x1:x2]

    image = Image.fromarray(face)
    image = image.resize(size)

    return np.asarray(image)


