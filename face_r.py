import face_recognition
import cv2
import numpy as np
import os
import sys
import time

# from face_r import learn, recognice
# recognice(3, learn())

def learn():
    # Iterate over folder of faces and create arrays of known face encodings and their names
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
    return [known_face_encodings, known_face_names]

# pass in times to recognice and known_face_names and known_face_encodings
# Improve: store faces in database and learn oly when neccessary
def recognice(times, known):
    # plug in known face_encoding and face_names
    known_face_encodings = known[0]
    known_face_names = known[1]

    # Initialize default #0 camera
    video_capture = cv2.VideoCapture(0)
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

# Declare main function
def main():
    recognice(3, learn())

if __name__ == '__main__':
    # Run from console
    main()
