"""This is facecam module.

Recognizes faces for Baari-Mikko.
"""


import face_recognition
import cv2
import numpy as np
import threading
import pickle
import hashlib
import pandas as pd
from collections import Counter
import time


lock = threading.Lock()


class CameraStream:
    """
    Camera object.
    TODO: commenting
    """
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        self.int = 1

    def start(self):
        # start the thread to read frames from the video stream
        threading.Thread(target=self.update, args=()).start()
        print(f'Camera thread {self.int} running')
        self.int += 1
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            time.sleep(0.030)

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


# Learns faces and inserts user into database
def learn(name, img_path):
    """
    Creates n-dimensional face mappings in pickled format to store in database
    :param name: Username str
    :param img_path: Image name str
    :return: Pickled face mapping
    """
    # learn face and insert into database
    try:
        if img_path.endswith(".jpg"):
            face = face_recognition.load_image_file('faces/'+img_path)
            face_encoding = face_recognition.face_encodings(face)[0]
            pickled = pickle.dumps(face_encoding)

            # result = create_user(name, pickled, img_path, admin_boolean)

            print(name+" learned and stored to db.")
            return pickled

    except Exception as e:
        print(f"The error '{e}' occurred")


# Camera feed to frontend
# yields jpg frames
def feed(vs):
    while True:
        frame = vs.read()
        asd, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0.030)


# IMPROVE: update to multithreaded to increse speed and accuracy
# compares camera frames x(times) to face database
# GETS: times (int, how many frames to recognize faces agains)
# RETURNS: name (str, most appeared name in frame(s))
def compare(times, users, vs):
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
        frame = vs.read()

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
def capture(img_name, vs):
    # hashes filename(username) to avoid any problem with caracters
    img_hash = hashlib.md5(img_name.encode('utf-8')).hexdigest()
    image = vs.read()
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
    """
    Create root user with admin rights
    """
    from databaseinterface import DatabaseInterface
    from databasequeries import DatabaseQueries as Dbq
    dbi = DatabaseInterface("test1", "mikko", "baari", "127.0.0.1")
    username = 'root'
    img_path = 'root.jpg'
    print('Create root user from faces/root.jpg')
    ask = input('Y/N?')
    if ask in ('Y', 'y', 'yes', 'Yes', 'YES'):
        try:
            pickled = learn(username, img_path)
            args = (username, pickled, img_path, True)
            dbi.execute_query(Dbq.CREATE_USER, args)
        except Exception as e:
            print(e)
    else:
        print('cancelled by user')
