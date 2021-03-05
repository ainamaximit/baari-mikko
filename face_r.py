import face_recognition
import cv2
import numpy as np
import os
import sys
import time
import threading

startTime = time.time()

# from face_r import recognize
# recognize(5)

# Declare queue and its methods
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self, data):
        data = None
        try:
            data = self.queue.pop(0)
        except IndexError as ex:
            pass
        return data

    def is_empty(self):
        return len(self.queue) == 0

# Create queues for threads
q1 = Queue()
q2 = Queue()

def learn(x):
    # Iterate over folder of faces and create arrays of known face encodings and their names
    print('Learning initialize.')
    known_face_encodings = []
    known_face_names = []
    directory = r'faces'
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Load a sample picture and learn how to recognize it.
            face = face_recognition.load_image_file('faces/'+filename)
            face_encoding = face_recognition.face_encodings(face)[0]

            # Add known face encodings and their names to correponding arrays
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])
        else:
            continue

    print('Learned ',len(known_face_names), ' face(s).')
    known = [known_face_encodings, known_face_names]
    return known

# pass in times to recognice and known_face_names and known_face_encodings
# Improve: store faces in database and learn oly when neccessary
def camera(x):
    print('Camera initialize.')
    video_capture = cv2.VideoCapture(0)
    print('Camera ready.')
    return video_capture

def compare(times, known, video_capture):
    # plug in known face_encoding and face_names
    known_face_encodings = known[0]
    known_face_names = known[1]

    # Initialize default #0 camera
    for i in range(times):
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if not face_locations:
            name = "no_face"

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "unknown"

            # Find best match for the known face(s)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        print(name)

    # Release handle to the webcam
    video_capture.release()

    # Improve: validate over multiple recognitions instead of the last one
    return name

# Threaded
def recognize(times):
    # Face learning thread
    t1 = threading.Thread(target=lambda q1, arg: q1.enqueue(learn(arg)), args=(q1,1))

    # Camera thread
    t2 = threading.Thread(target=lambda q2, arg: q2.enqueue(camera(arg)), args=(q2,1))

    # Start threads
    t1.start()
    t2.start()

    # Wait for threads to finish
    t1.join()
    t2.join()

    # Take photos x times to compare
    name = compare(times,q1.dequeue(learn),q2.dequeue(camera))

    print(time.time() - startTime)

    return name
# Non threaded
def recognize_sync(times):
    name = compare(times,learn(1),camera(1))
    print(time.time() - startTime)

    return name
if __name__ == '__main__':
    # Run from console and take 5 photos to compare
    recognize(5)
    # recognize_sync(5)
