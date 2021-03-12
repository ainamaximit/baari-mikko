import face_recognition
import cv2
import numpy as np
import os
import sys
import time
import threading
import pickle
import hashlib
from collections import Counter
from db_query import create_user, get_users_faces

global global_camera

# Learns faces and inserts user into database
def learn(name, img_path):
    # learn face and insert into database
    try:
        if img_path.endswith(".jpg"):
            face = face_recognition.load_image_file('faces/'+img_path)
            face_encoding = face_recognition.face_encodings(face)[0]
            pickled = pickle.dumps(face_encoding)

            result = create_user(name, pickled, img_path)

            print(name+" learned and stored to db.")
            print(result)
            return True

    except Exception as e:
        print(f"The error '{e}' occurred")

# Create camera object and pass it along
def camera_on():
    try:
        print('Camera initialize.')
        video_capture = cv2.VideoCapture(0)
        print('Camera ready.')
        return video_capture
    except Exception as e:
        print(f"The error '{e}' occurred")

# Create global camera object and turn camera on at app launch
# IMPROVE: This might be unstable method. Should use lock?
global_camera = camera_on()

# Camera feed to frontend
# yields jpg frames
# IMPROVE: should use lock to avoid simultanous read and write
def camera_feed():
    # Enter to endless loop while feed open
    while True:
        # Read camera frame
        success, frame = global_camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

# IMPROVE: update to multithreaded to increse speed and accuracy
# compares camera frames x(times) to face database
# GETS: times (int, how many frames to recognize faces agains)
# RETURNS: name (str, most appeared name in frame(s))
def compare(times):
    startTime = time.time()
    # plug in known face_encoding and face_names
    try:
        known_face_encodings = []
        known_face_names = []
        x=0
        users = get_users_faces()

        # get names and faces from database to dict
        # pickle converts bytes data back to n-dimensional array
        for user in users:
            pickled = users[x][2]
            known_face_encodings.append(pickle.loads(pickled))
            known_face_names.append(users[x][1])
            x+=1

    except Exception as e:
        print(f"The error '{e}' occurred")

    # Initialize default #0 camera
    names = []
    for i in range(times):
        # Grab a single frame of video
        ret, frame = global_camera.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if not face_locations:
            names.append("denied")

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # Find best match for the known face(s)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                names.append(known_face_names[best_match_index])
            else:
                names.append("denied")

    # Release handle to the webcam
    # video_capture.release()

    # Rerurn most common recognizez name in names
    occurence_count = Counter(names)
    name = occurence_count.most_common(1)[0][0]

    # Calculate time to run compare() and round it to ms
    timer = time.time()-startTime
    print('Facecam compare() runtime '+round(timer, 3)+' s')

    # return most common name in recognized frames
    return name

# Captures photo and saves it to faces
# Returns file name
def capture(img_name):
    # hashes filename(username) to avoid any problem with caracters
    img_hash = hashlib.md5(img_name.encode('utf-8')).hexdigest()
    return_value, image = global_camera.read()
    cv2.imwrite('faces/'+img_hash+'.jpg', image)
    # returns filename
    return img_hash+'.jpg'

if __name__ == '__main__':
