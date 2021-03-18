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
    def __init__(self, src=0):
        """
        Creates camera object and reads first frame from the camera.
        :param src: int, Camera in cv2 default is 0
        """
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.fps = 0.03
        self.int = 1

    def start(self):
        """
        Creates camera instance
        :return: self
        """
        threading.Thread(target=self.update, args=()).start()
        print(f'Camera thread {self.int} running')
        self.int += 1
        return self

    def update(self):
        """
        Reads frames from camera endlessly until stopped and stores latest to self.frame
        :return: None
        """
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()
            time.sleep(self.fps)  # Sleep to reduce cycle speed (fps)

    def read(self):
        """
        Use this to get latest frame from camera.
        :return: frame (cv2)
        """
        return self.frame

    def stop(self):
        """ Call this to stop the camera thread """
        self.stopped = True


# Learns faces and inserts user into database
def learn(name, image_path):
    """
    Creates n-dimensional face mappings in pickled format to store in database
    :param name: Username str
    :param image_path: Image name str
    :return: Pickled face mapping
    """
    # learn face and insert into database
    try:
        if image_path.endswith(".jpg"):
            face = face_recognition.load_image_file('faces/'+image_path)
            face_encoding = face_recognition.face_encodings(face)[0]
            pickled_face = pickle.dumps(face_encoding)
            print(name+" learned and stored to db.")
            return pickled_face

    except Exception as error:
        print(f"The error '{error}' occurred in facecam.py learn()")


# Camera feed to frontend
# yields jpg frames
def feed(vs):
    """
    Video stream from camera object.
    :param vs: Camera object
    :return: MotionJPEG stream
    """
    while True:
        frame = vs.read()
        asd, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        time.sleep(0.030)


def compare(times, users, vs):
    """
    Uses facial recognition to identify pre-learned faces.
    TODO: Multiprocessing to speed up login (possible 4x improvement)
    :param times: int, How many frames to recognize
    :param users: 2 lists in list, User names and face codings
    :param vs: Camera object
    :return: str, users name or denied
    """
    # set variables
    known_face_encodings = []
    known_face_names = []
    x = 0

    try:
        # get names and faces from database to dict
        # pickle converts bytes data back to n-dimensional array
        for user in users:
            pickled_face = users[x][2]
            known_face_encodings.append(pickle.loads(pickled_face))
            known_face_names.append(users[x][1])
            x += 1

    except Exception as error:
        print(f"The error '{error}' occurred in facecam.py compare() parse users")

    # Initialize default #0 camera
    names = []
    for i in range(times):
        # Grab a single frame of video
        frame = vs.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the frame of video
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

    # Return most common recognizes name in names
    occurrence_count = Counter(names)
    name = occurrence_count.most_common(1)[0][0]

    # return most common name in recognized frames
    return name


# Captures photo and saves it to faces
def capture(img_name, vs):
    """
    Captures photo and saves it to faces folder
    :param img_name: str, file name to hash md5
    :param vs: Camera object
    :return: img file name
    """
    # hashes filename(username) to avoid any problem with characters
    img_hash = hashlib.md5(img_name.encode('utf-8')).hexdigest()
    image = vs.read()
    cv2.imwrite('faces/'+img_hash+'.jpg', image)
    # returns filename
    return img_hash+'.jpg'


def get_camera_resolutions():
    """
    Prints supported camera resolutions
    :return: None
    """
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
    Create root user with admin rights from provided root.jpg
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
            print(f"Error {e} while creating root user. Did you provide faces/root.jpg and is database set correctly?")
    else:
        print('Cancelled by user')
        exit(0)
