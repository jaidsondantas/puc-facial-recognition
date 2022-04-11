import json
from operator import attrgetter
import os
from random import random

import face_recognition
from flask import request
import numpy as np
from bd import cursor, db
from flask_restful import Resource, reqparse
from PIL import Image, ImageDraw, ImageFont
from utils.extract import extract_faces
import uuid
from config import config
from flask import Flask


from resources.services import treatamentPhoto


class Photo(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument('person')

    def put(self, photo_id):
        data = Photo.attributes.parse_args()
        print(data)

        query = "UPDATE photos SET person=" + \
            data['person'] + " WHERE id=" + photo_id
        cursor.execute(query)
        db.commit()

        return {"status": "success"}


#
#
#
#
#
# Create Photos
#
#
#
#
#
#
class Photos(Resource):

    def post(self):
        files = request.files
        if files:
            file = files['file']
            filename = str(uuid.uuid4()) + ".jpg"
            file.save(os.path.join(config.UPLOAD_FOLDER, filename))

            photo = face_recognition.load_image_file(
                os.path.join(config.UPLOAD_FOLDER, filename))

            photo_np = np.asarray(photo)
            photo_np = Image.fromarray(photo_np)
            photo_np = photo_np.resize((640, 640))
            pil_image = photo_np
            draw = ImageDraw.Draw(pil_image)

            found_faces, face_locations = extract_faces(photo_np)
            lasts = []
            face_encodings = []

            if len(found_faces):

                for face in found_faces:
                    enc = treatamentPhoto.encoding_photo(face)

                    if len(enc):
                        face_encodings.append(enc)

                photos = generateImagePreview(
                    face_locations, face_encodings, draw)
                lasts = photos
            # Remove the drawing library from memory as per the Pillow docs
            del draw

            # Display the resulting image
            # pil_image.show()
            filename = str(uuid.uuid4())

            pil_image.save("./static\\" + filename + ".jpeg", "JPEG")

            return {
                "photo": "static/" + filename + ".jpeg",
                "people": lasts
            }

    def get(self):
        cursor.execute("SELECT * FROM photos")
        photos = cursor.fetchall()

        return photos

#
#
#
# Functions Publics
#
#
#


def insertPhoto(enc, person, precision):

    precision = 1 - precision

    query = "INSERT INTO photos (matriz, person, photos.precision) VALUES (%s, %s, %s)"
    if person:
        tuple = (json.dumps(enc[0].tolist()), person['id'], precision)
    else:
        tuple = (json.dumps(enc[0].tolist()), 0, precision)

    cursor.execute(query, tuple)
    db.commit()

    querySelect = "SELECT id, person, photos.precision from photos where photos.id = LAST_INSERT_ID()"
    cursor.execute(querySelect)

    return cursor.fetchone()


def getFaceEncodings():
    query = 'select ph.id as id_photo, matriz, person, p.id as id_person, ph.precision, name from photos as ph INNER JOIN people as p on  ph.person = p.id'
    cursor.execute(query)
    photos = cursor.fetchall()

    encs = []
    for photo in photos:
        encs.append(json.loads(photo["matriz"]))

    return encs, photos


def generateImagePreview(face_locations, face_encodings, draw):

    known_face_encodings, photos = getFaceEncodings()
    photosAdded = []
    i = 0

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        color_background = (0, 255, 0)
        bottom += 20
        i += 1
        if len(face_encoding):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding[0], tolerance=0.40)
            name = "Desconhecido" + str(i)

            # Or instead, use the known face with the smallest distance to the new fac
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding[0])

            if len(face_distances):
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    person = {
                        "name": photos[best_match_index]['name'],
                        "id": photos[best_match_index]['id_person']
                    }

                    photo = insertPhoto(
                        face_encoding, person, face_distances[best_match_index])
                    photo['person'] = person
                    name = photos[best_match_index]['name'] + \
                        " " + str(photo["id"])
                    photosAdded.append(photo)
                else:
                    person = {
                        "id": 0,
                        "name": "Desconhecido"
                    }
                    photo = insertPhoto(face_encoding, None,
                                        face_distances[best_match_index])
                    photo["person"] = person

                    photosAdded.append(photo)
                    name = "Desconhecido " + str(photo['id'])
            else:
                person = {
                    "id": 0,
                    "name": "Desconhecido"
                }
                photo = insertPhoto(face_encoding, None, 0)
                photo["person"] = person
                photosAdded.append(photo)
                name = "Desconhecido " + str(photo['id'])

        draw.rectangle(((left, top), (right, bottom)),
                       outline=color_background)

        # Draw a box around the face using the Pillow module
        font = ImageFont.truetype("arial.ttf", 16)

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)),
                       fill=color_background, outline=color_background)
        draw.text((left + 6, bottom - text_height - 5),
                  name, fill=(0, 0, 0, 255), font=font)

    return photosAdded
