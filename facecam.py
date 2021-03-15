import face_recognition
import cv2
import numpy as np
import threading
import pickle
import hashlib
import pandas as pd
from collections import Counter

lock = threading.Lock()


# Learns faces and inserts user into database
def learn(name, img_path, admin):
    # learn face and insert into database
    try:
        if img_path.endswith(".jpg"):
            face = face_recognition.load_image_file('faces/'+img_path)
            face_encoding = face_recognition.face_encodings(face)[0]
            pickled = pickle.dumps(face_encoding)
            admin_boolean = False
            print(admin)
            if admin == 'on':
                admin_boolean = True

            result = create_user(name, pickled, img_path, admin_boolean)

            print(name+" learned and stored to db.")
            print(result)
            return True

    except Exception as e:
        print(f"The error '{e}' occurred")


# Create global camera object and turn camera on at app launch
# IMPROVE: This might be unstable method. Should use lock?
class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)  # Use res.py to get supported resolutions
        self.cap.set(4, 480)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

    def read(self):
        return self.cap.read()


global video_camera
video_camera = VideoCamera()


# Camera feed to frontend
# yields jpg frames
def feed(video_camera):
    if video_camera is None:
        video_camera = VideoCamera()
    while True:
        with lock:
            frame = video_camera.get_frame()

            if frame is not None:
                global_frame = frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# IMPROVE: update to multithreaded to increse speed and accuracy
# compares camera frames x(times) to face database
# GETS: times (int, how many frames to recognize faces agains)
# RETURNS: name (str, most appeared name in frame(s))
def compare(times, users):
    # plug in known face_encoding and face_names
    try:
        known_face_encodings = []
        known_face_names = []
        x = 0

        # get names and faces from database to dict
        # pickle converts bytes data back to n-dimensional array
        for user in users:
            pickled = users[x][2]
            known_face_encodings.append(pickle.loads(pickled))
            known_face_names.append(users[x][1])
            x += 1

    except Exception as e:
        print(f"The error '{e}' occurred")

    # Initialize default #0 camera
    names = []
    for i in range(times):
        # Grab a single frame of video
        ret, frame = video_camera.read()

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

    # return most common name in recognized frames
    return name


# Captures photo and saves it to faces
# Returns file name
def capture(img_name):
    # hashes filename(username) to avoid any problem with caracters
    img_hash = hashlib.md5(img_name.encode('utf-8')).hexdigest()
    return_value, image = video_camera.read()
    cv2.imwrite('faces/'+img_hash+'.jpg', image)
    # returns filename
    return img_hash+'.jpg'


def get_camera_resolutions():
    url = "https://en.wikipedia.org/wiki/List_of_common_resolutions"
    table = pd.read_html(url)[0]
    table.columns = table.columns.droplevel()

    cap = cv2.VideoCapture(0)
    resolutions = {}

    for index, row in table[["W", "H"]].iterrows():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, row["W"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, row["H"])
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        resolutions[str(width)+"x"+str(height)] = "OK"

    print(resolutions)


if __name__ == '__main__':
    username = input()
    img_path = capture(username)
    # lear returns boolean
    # learn learns captured image and saves face mappings to database
    response = learn(username, img_path)
