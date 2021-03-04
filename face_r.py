import face_recognition
import cv2
import numpy as np
import os
import sys
import time

# Usage: is somewhat broken still
# from face_r import face_r

def face_r():
    # Initialize default #0 camera
    video_capture = cv2.VideoCapture(0)
    video = False

    if len(sys.argv)>=2:
        if sys.argv[1] == '--video':
            video = True
            print('Live video mode only')

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

    print('Known faces ',known_face_names)

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if not face_locations:
            name = None

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

            # if --video argument is set draw image
            if video:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            else:
                continue
        # if --video argument is set render image
        if video:
            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print(name)
            # return name
            time.sleep(1)

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

def main():
    face_r()

if __name__ == '__main__':
    main()
