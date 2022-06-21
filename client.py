import face_recognition
import cv2
import numpy as np
import os, sys
import pickle

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from django.core.exceptions import ValidationError


def face_detect(image):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    filesize = (image.size)
    if filesize > 5242880:  # 5 MiB in bytes
        response = {"result": "The maximum file size that can be uploaded is 5 MiB"}
    else:
        try:

            with open('face_encoding.pickle', 'rb+') as handle:
                load_data = pickle.load(handle)

            name = "Unknown"
            known_face_encodings = load_data["face_encodings"]
            known_face_names = load_data["user_names"]
            print(len(known_face_encodings),len(known_face_names))
            print(known_face_names)

            image_path = default_storage.save("tmp/tmp.jpg", ContentFile(image.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, image_path)

            img = cv2.imread(tmp_file)
            img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
            # img = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(img)
            face_encodings = face_recognition.face_encodings(img, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
            
            default_storage.delete(tmp_file)

            if name == "Unknown":
                response = {"result": "No Match Found! Please Register"}
            else:
                response = {"result": name}
        except:
            response = {"result": "Server Error"}

    return response

def face_check(tmp_file):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    try:

        with open('face_encoding.pickle', 'rb+') as handle:
            load_data = pickle.load(handle)

        name = "Unknown"
        known_face_encodings = load_data["face_encodings"]
        known_face_names = load_data["user_names"]
        print(len(known_face_encodings),len(known_face_names))
        print(known_face_names)

        img = cv2.imread(tmp_file)

        face_locations = face_recognition.face_locations(img)
        face_encodings = face_recognition.face_encodings(img, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        if name == "Unknown":
            response = {"username": "No Match Found! Please Register"}
        else:
            response = {"username": name}
    except:
        response = {"username": "Server Error"}

    return response

def face_enrollment(image, name):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    filesize = (image.size)
    if filesize > 5242880:  # 5 MiB in bytes
        response = {"result": "The maximum file size that can be uploaded is 5 MiB"}
    else:
        # try:
        # change this as you see fit
        try:
            with open('face_encoding.pickle', 'rb+') as handle:
                load_data = pickle.load(handle)

            known_face_encodings = load_data["face_encodings"]
            known_face_names = load_data["user_names"]
        except:
            known_face_encodings = []
            known_face_names = []
        
        image_path = default_storage.save("tmp/temp.jpg", ContentFile(image.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, image_path)

        result = face_check(tmp_file)

        if result['username'] in known_face_names:
            response = {"result": "User already exists!"}
        else:
            load_image = face_recognition.load_image_file(tmp_file)
            # load_image = cv2.imread(tmp_file)
            # height, width, channels = load_image.shape
            # if height or width > 720:
            #     small_frame = cv2.resize(load_image, (0, 0), fx=0.25, fy=0.25)
            #     load_image = small_frame[:, :, ::-1]
            print(load_image)
            

            face_encoding = face_recognition.face_encodings(load_image)[0]

            # Create arrays of known face encodings and their names
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)

            store_data = {"face_encodings" : known_face_encodings,"user_names": known_face_names}

            with open(f'face_encoding.pickle', 'wb+') as handle:
                pickle.dump(store_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
                
            response = {"result": "Enrollment Successful"}
        default_storage.delete(tmp_file)
        # except:
        #     response = {"result": "Enrollment Unsuccessful"}

    return response