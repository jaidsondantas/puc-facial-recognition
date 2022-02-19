import json

import face_recognition
from bd import cursor, db
from flask_restful import Resource
from utils.extract import extract_faces

from resources.services import treatamentPhoto


class Photo(Resource):
    def post(self):
        photo = face_recognition.load_image_file("storage/19022022.jpg")

        facesFound, face_locations = extract_faces(photo)
        lasts = []

        if len(facesFound):

            for face in facesFound:
                enc = treatamentPhoto.encoding_photo(face)

                if len(enc):
                    insertPhoto(enc)
                    lasts.append(cursor.fetchone())

        return lasts

    def get(self):
        cursor.execute("SELECT * FROM photos")
        photos = cursor.fetchall()

        return photos


def insertPhoto(enc):
    query = "INSERT INTO photos (matriz, person) VALUES (%s, %s)"
    tuple = (json.dumps(enc[0].tolist()), 0)

    cursor.execute(query, tuple)
    db.commit()

    querySelect = "SELECT id, person from photos where photos.id = LAST_INSERT_ID()"
    cursor.execute(querySelect)
