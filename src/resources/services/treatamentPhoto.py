import face_recognition


def encoding_photo(face):
    enc = face_recognition.face_encodings(face, model='cnn')

    if not len(enc):
        location = face_recognition.face_locations(
            face, model='cnn')
        enc = face_recognition.face_encodings(
            face, known_face_locations=location, model='cnn')

    return enc
